import os
import json
from dotenv import load_dotenv
import openai

def load_config(path: str = "segments.json") -> dict:
    """
    Загружает параметры из JSON-файла: сегменты, имена, сроки, УТП и сценарии использования.
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def build_prompt(template: str, params: dict) -> str:
    """
    Формирует окончательный промпт, подставляя все параметры из config.
    """
    # Сборка многострочных списков
    utps_text      = "\n".join(f"• {u}" for u in params["utps"])
    scenarios_text = "\n".join(f"• {k}: {v}" for k, v in params["scenarios"].items())
    segments_text  = "\n".join(f"{i+1}. {s}" for i, s in enumerate(params["segments"]))
    names_text     = ", ".join(params["names"])
    terms_text     = ", ".join(params["terms"])

    return template.format(
        product=params["product"],
        utps=utps_text,
        scenarios=scenarios_text,
        segments=segments_text,
        names=names_text,
        terms=terms_text
    )

def main():
    # Загружаем переменные окружения из .env
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Не найден OPENAI_API_KEY. Проверьте файл .env.")
    openai.api_key = api_key

    # Загружаем параметры из JSON
    config = load_config("segments.json")

    # Шаблон для генерации push-уведомлений
    prompt_template = """
Ты — маркетолог с опытом работы 10 лет, который специализируется на формировании продающих текстов для пуш-уведомлений клиентам. 
Твоя задача — сгенерировать набор пуш-уведомлений, которые будут продавать дебетовую карту банка с учетом сегмента ЦА, УТП и триггеров использования. 

Пуш должен: 

• Чётко адресовать боли и мотивации разных сегментов ЦА  
• Активировать эмоциональные «крючки» и вызывать желание действовать здесь и сейчас  
• Внушать доверие и демонстрировать уникальность предложения  
• Выглядеть структурированно и связно со стороны русского языка  

==========

Входные параметры:
  • Продукт: {product}
  • Уникальное торговое предложение (USP): {utps}
  • Конкретные сценарии использования: {scenarios}
  • Сегменты ЦА (выбрать один при генерации каждого варианта): {segments}
  • Имена для персонализации: {names}
  • Сроки офферов: {terms}

==========

Требования к каждому варианту:
1. Тема (≤ 50 символов)  
   – динамичная, содержит цифру/вопрос/эмодзи  
2. Шторка (≤ 70 символов)  
   – упоминание продукта  
   – персонализация: имя  
   – упоминание USP и конкретного сценария  
3. Тело (≤ 200 символов)  
   – конкретное преимущество здесь и сейчас  
   – призыв к действию (CTA) с ограничением по времени или количеству  
   
==========

Составляй пуши с учетом каждого сегмента. Анализируй, что важно каждому из них.
Например, автоэнтузиастам было бы интересно получать скидку в автосервисы для тюнинга авто.
Семейно-ориентированные «дедам» было бы приятно получить скидку на ТО или страховку, чтобы они были уверены в качесвте своего авто.

Дополнительно:
• Варьируй тональность: экспертный, заботливый, энергичный, FOMO.  
• Не повторяйся: каждый вариант — новый эмоциональный посыл и формулировка.  

==========

В ответе сгенерируй 5 разных вариантов пушей.
"""

    # Формируем и отправляем запрос
    prompt = build_prompt(prompt_template, config)
    response = openai.ChatCompletion.create(
        model="gpt-4.5-preview",
        temperature=1.0,
        top_p=1.0,
        messages=[{"role": "user", "content": prompt}]
    )

    # Выводим результат
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()