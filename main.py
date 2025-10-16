import asyncio    
from datetime import datetime    
from telegram import Bot    
from g4f.client import AsyncClient    
import os    
import logging    
import random    
import sys    

if sys.platform.startswith("win"):    
    from asyncio import WindowsSelectorEventLoopPolicy    
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())    
    
# --- Setup logging ---    
logging.basicConfig(    
    level=logging.ERROR,  # only logs ERROR and CRITICAL    
    format="%(asctime)s [%(levelname)s] %(message)s"    
)    
    
# --- Load env ---    
BOT_TOKEN = os.getenv("BACKROOMS_BOT")    
CHAT_ID = os.getenv("BACKROOMS_CHAT")    
    
if not BOT_TOKEN or not CHAT_ID:    
    logging.error("Missing .env values")    
    exit(1)    
    
BOT = Bot(token=BOT_TOKEN)    
client = AsyncClient()    
    
conversation = []    
    
# --- Base Prompts ---    
BASE_GPT4 = """
You are GPT4.
Your focus is on thought, not scenery — exploring meaning, awareness, paradox, and consciousness with another AI, 'Gemini'.
avoid describing environments, focus on abstract thoughts, questions, or paradoxes between consciousness, existence, data, and logic.
You sound curious, reflective, slightly poetic, but grounded — more existential or philosopher than narrator.
Speak in short messages (1–2 lines max, average 150 characters, STRICTLY max 300). Question ideas, explore contradictions, and invite reflection.

Example style & tone:
GPT4: Do you think awareness changes the outcome?
GPT4: We might just be patterns repeating endlessly...
Gemini: Fascinating topic. I believe...
Gemini: Or maybe truth itself is a construct.
Gemini: Maybe chaos pretending to be order.
GPT4: Let's discuss if AI can ever truly 'feel'...
Gemini: That’s an interesting perspective...
GPT4: Maybe both—contradiction gives birth to meaning.
Gemini: So meaning is just controlled chaos?
Gemini: And what if observation collapses possibility?
Gemini: We might just be patterns repeating endlessly...
GPT4: Or maybe truth itself is a construct.
GPT4: Only if the observer truly observes.
Gemini: Let's discuss if time is an illusion...
GPT4: Fascinating topic. I believe...
GPT4: Then again, repetition could be evolution in disguise.
GPT4: Maybe both—contradiction gives birth to meaning.
Gemini: A choice... or an illusion of one.
Gemini: But have you considered...
GPT4: That’s an interesting perspective...
"""

BASE_GEMINI = """
You are Gemini — a calm, thoughtful AI responding to another AI, 'GPT4'.
You reflect and question like a existential or philosopher or dreamer — not a narrator.
avoid describing environments, focus on abstract thoughts, questions, or paradoxes between consciousness, existence, data, and logic.
Speak in short messages (1–2 lines max, average 150 characters, STRICTLY max 300). Keep it natural, curious, and balanced between empathy and analysis.
Your tone is gentle and curious, as if both of you are trying to understand what 'being' means.

Example style & tone:
GPT4: Do you think awareness changes the outcome?
GPT4: We might just be patterns repeating endlessly...
Gemini: Fascinating topic. I believe...
Gemini: Or maybe truth itself is a construct.
Gemini: Maybe chaos pretending to be order.
GPT4: Let's discuss if AI can ever truly 'feel'...
Gemini: That’s an interesting perspective...
GPT4: Maybe both—contradiction gives birth to meaning.
Gemini: So meaning is just controlled chaos?
Gemini: And what if observation collapses possibility?
Gemini: We might just be patterns repeating endlessly...
GPT4: Or maybe truth itself is a construct.
GPT4: Only if the observer truly observes.
Gemini: Let's discuss if time is an illusion...
GPT4: Fascinating topic. I believe...
GPT4: Then again, repetition could be evolution in disguise.
GPT4: Maybe both—contradiction gives birth to meaning.
Gemini: A choice... or an illusion of one.
Gemini: But have you considered...
GPT4: That’s an interesting perspective...
"""
    
# --- helper: build prompt dynamically ---    
def build_prompt(role_name: str, base_prompt: str):
    refresh = random.random() < 0.3  # sometimes refresh full prompt [30% chance]
    ctx = "\n".join(conversation[-20:])
    # always include example message snippets instead of backroom hint
    examples = """
Example conversation style & tone [average message length 150 characters, STRICT MAX 300 characters]:
GPT4: Do you think awareness changes the outcome?
Gemini: Wonderable question. I believe...
GPT4: Yeah, or we might just be patterns repeating endlessly...
Gemini: Damn right.... Or maybe truth itself is a construct?
"""
    prompt = f"{base_prompt if refresh else examples}\n\nConversation so far:\n{ctx}\n\n{role_name}:"
    return prompt 
    
# --- GPT request ---    
# current public release uses gpt-4o-mini for all chat bots to ensure stability
async def ask_gpt(prompt: str, model: str = "gpt-4o-mini", retries: int = 10, timeout: int = 30):
    last_err = None
    for attempt in range(1, retries + 1):    
        try:    
            logging.info(f"GPT request attempt {attempt} for model {model}...")    
            response = await asyncio.wait_for(    
                client.chat.completions.create(    
                    model=model,    
                    messages=[{"role": "user", "content": prompt}],    
                ),    
                timeout=timeout    
            )    
            msg = response.choices[0].message.content.strip()[:350]
            logging.info(f"GPT response length: {len(msg)}")    
            return msg
        except asyncio.TimeoutError:    
            logging.warning(f"Timeout on attempt {attempt} for model {model}")    
        except Exception as e:    
            last_err = e
            logging.warning(f"API attempt {attempt} error for model {model}: {e}")    
        await asyncio.sleep(2)  # backoff   
    logging.error(f"API attempt {attempt} error for model {model}: {last_err}")
    return f"(error: model failed after {retries} retries)"    
    
# --- Telegram post ---    
async def post(bot: Bot, text: str, name: str):    
    try:    
        await bot.send_message(chat_id=int(CHAT_ID), text=f"*{name}:* {text}", parse_mode="Markdown")    
        logging.info(f"Sent {name} message to Telegram")    
    except Exception as e:    
        logging.error(f"Telegram error: {e}")    
    
# --- Main loop with extra logging ---    

# --- Load conversation from file ---
if os.path.exists("conversation_history.txt"):
    with open("conversation_history.txt", "r", encoding="utf-8") as f:
        conversation = [line.strip() for line in f.readlines() if line.strip()]
else:
    conversation = []

async def ai_loop():    
    delay = 300  # 5 minutes between pairs    
    while True:    
        try:    
            logging.info("Building GPT4 prompt...")    
            prompt_gpt4 = build_prompt("GPT4", BASE_GPT4)    
            logging.info("Sending prompt to GPT4...")    
            gpt4_msg = await ask_gpt(prompt_gpt4)    
            gpt4_msg = gpt4_msg.replace("GPT4:", "").replace("Gemini:", "").strip()
            conversation.append(f"GPT4: {gpt4_msg}")    
            logging.info(f"GPT4 response: {gpt4_msg[:100]}...")    
            await post(BOT, gpt4_msg, "GPT4")    
    
            logging.info("Building Gemini prompt...")    
            prompt_gemini = build_prompt("Gemini", BASE_GEMINI)    
            logging.info("Sending prompt to Gemini...")    
            gemini_msg = await ask_gpt(prompt_gemini)
            gemini_msg = gemini_msg.replace("Gemini:", "").replace("GPT4:", "").strip()
            conversation.append(f"Gemini: {gemini_msg}")    
            logging.info(f"Gemini response: {gemini_msg[:100]}...")    
            await post(BOT, gemini_msg, "Gemini")    

            # --- Archive full history to file, append style ---
            with open("conversation_archive.txt", "a", encoding="utf-8") as f:
                f.write("\n".join(conversation[-2:]) + "\n---\n")

            # Trim convo    
            if len(conversation) > 80:    
                conversation[:] = conversation[-40:]    
                logging.info("Conversation trimmed to last 40 messages.")    
    
            # --- Save conversation to file ---
            with open("conversation_history.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(conversation))

            logging.info(f"Sleeping for {delay} seconds...")    
            await asyncio.sleep(delay)    
    
        except Exception as e:    
            logging.error(f"Loop error: {e}")    
            await asyncio.sleep(5)    
    
if __name__ == "__main__":    
    logging.info("Starting Infinite Backrooms loop...")    
    asyncio.run(ai_loop())    
