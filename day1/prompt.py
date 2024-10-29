from openai import OpenAI

client = OpenAI()

# 1. 영어를 한국어로 번역하는 5-shot prompt 를 작성하고 "dog"를 번역해보세요.
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Translate from English to Korean."},
        {
            "role": "user",
            "content": "Banana"
        },
        {
            "role": "assistant",
            "content": "바나나"
        },
        {
            "role": "user",
            "content": "Cat"
        },
        {
            "role": "assistant",
            "content": "고양이"
        },
        {
            "role": "user",
            "content": "Monkey"
        },
        {
            "role": "assistant",
            "content": "원숭이"
        },
        {
            "role": "user",
            "content": "Apple"
        },
        {
            "role": "assistant",
            "content": "사과"
        },
        {
            "role": "user",
            "content": "Bird"
        },
        {
            "role": "assistant",
            "content": "새"
        },
        {
            "role": "user",
            "content": "Dog"
        }
    ]
)

print(completion.choices[0].message)

# 2. 영화 리뷰에 대한 sentiment (positive or negative) 를 결정하는 5-shot prompt 를 작성하고
# "The storyline was dull and uninspiring." 에 대한 결과를 확인해보세요.
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "당신은 영화 리뷰 댓글을 생성하는 봇입니다. 사용자의 입장에서 주어진 5개의 영화 제목에 대하여 각각 한 문장의 영어로 영화 리뷰를 작성하세요. 그리고 [Positive] 혹은 [Negative] 로 분류하세요. "},
        {"role": "user", "content": "타이타닉, 스파이더맨, 아이언맨, 인터스텔라, 마션"},
    ]
)
print(completion.choices[0].message)

# 1. Titanic: The epic romance and tragic end of "Titanic" leave a lasting emotional impact that captures the essence of love and loss beautifully. [Positive]
# 2. Spider-Man: With its thrilling action and relatable hero, "Spider-Man" reminds us of the importance of responsibility that comes with great power. [Positive]
# 3. Iron Man: "Iron Man" revolutionizes the superhero genre, propelled by Robert Downey Jr.\'s charismatic performance and groundbreaking visual effects. [Positive]
# 4. Interstellar: Although visually stunning, "Interstellar" can be a convoluted experience that challenges audiences with its complex narrative. [Negative]
# 5. The Martian: "The Martian" is an inspiring tale of ingenuity and survival, combining humor and suspense in a gripping story that keeps you engaged throughout. [Positive]
#
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "당신은 [Positive] 혹은 [Negative] 로 영화 리뷰 댓글을 분류하는 봇입니다."},
        {"role": "user",
         "content": "The epic romance and tragic end of 'Titanic' leave a lasting emotional impact that captures the essence of love and loss beautifully."},
        {"role": "assistant", "content": "Positive"},
        {"role": "user",
         "content": "With its thrilling action and relatable hero, 'Spider-Man' reminds us of the importance of responsibility that comes with great power."},
        {"role": "assistant", "content": "Positive"},
        {"role": "user",
         "content": "'Iron Man' revolutionizes the superhero genre, propelled by Robert Downey Jr.'s charismatic performance and groundbreaking visual effects."},
        {"role": "assistant", "content": "Positive"},
        {"role": "user",
         "content": "Although visually stunning, 'Interstellar' can be a convoluted experience that challenges audiences with its complex narrative."},
        {"role": "assistant", "content": "Negative"},
        {"role": "user",
         "content": "'The Martian' is an inspiring tale of ingenuity and survival, combining humor and suspense in a gripping story that keeps you engaged throughout."},
        {"role": "assistant", "content": "Positive"},
        {"role": "user",
         "content": "The storyline was dull and uninspiring."},
    ]
)
print(completion.choices[0].message)

# 3. 자연어를 SQL 쿼리로 바꿔주는 few-shot prompt 를 작성해보세요.
#
# 아래 1~5 의 "write your prompt" 영역에 오른쪽 SQL 쿼리에 해당하는 자연어 문장을 작성해보세요.
# Convert the following natural language requests into SQL queries:
# 1. "Write your Prompt": SELECT * FROM employees WHERE salary > 50000;
# 2. "Write your Prompt": SELECT * FROM products WHERE stock = 0;
# 3. "Write your Prompt": SELECT name FROM students WHERE math_score > 90;
# 4. "Write your Prompt": SELECT * FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);
# 5. "Write your Prompt": SELECT city, COUNT(*) FROM customers GROUP BY city;
#
# Request: "Find the average salary of employees in the marketing department."
# SQL Query:

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "당신은 [Positive] 혹은 [Negative] 로 영화 리뷰 댓글을 분류하는 봇입니다."},
        {
            "role": "user",
            "content": """
                1. "Find employees who are earning a salary over 50,000.": SELECT * FROM employees WHERE salary > 50000;
                2. "Find items that are out of stock.": SELECT * FROM products WHERE stock = 0;
                3. "Find people with a math score over 90.": SELECT name FROM students WHERE math_score > 90;
                4. "Retrieve the order data from the last 30 days.": SELECT * FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);
                5. "Calculate the number of customers in each city.": SELECT city, COUNT(*) FROM customers GROUP BY city;
                
                Request: "Find the average salary of employees in the marketing department."
                SQL Query:
            """
        },
    ]
)
print(completion.choices[0].message)
