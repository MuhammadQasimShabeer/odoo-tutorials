import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PharmacyAIService(models.AbstractModel):
    _name = 'pharmacy.ai.service'
    _description = 'AI Service for Hugging Face'

    def _get_api_token(self):
        return self.env['ir.config_parameter'].sudo().get_param('HF_API_TOKEN')

    def _call_llm(self, messages, model="meta-llama/Llama-3.1-8B-Instruct:novita"):
        token = self._get_api_token()
        if not token:
            raise UserError(_("HF_API_TOKEN not set in system parameters."))

        API_URL = "https://router.huggingface.co/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messages": messages,
            "model": model,
            "temperature": 0.7,
            "max_tokens": 500
        }
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            raise UserError(_("AI service error: %s") % str(e))

    def analyze_sentiment(self, text):
        messages = [
            {"role": "system",
             "content": "You are a customer sentiment analyst. Respond ONLY with one word: Positive, Neutral, or Negative."},
            {"role": "user", "content": f"Analyze the sentiment of this feedback: '{text}'"}
        ]
        return self._call_llm(messages)

    def chat(self, user_message, conversation_history=None):
        messages = [
            {"role": "system",
             "content": "You are a helpful pharmacy assistant chatbot. Always remind users to consult a doctor for medical advice. Keep answers concise and friendly."},
            {"role": "user", "content": user_message}
        ]
        return self._call_llm(messages), []