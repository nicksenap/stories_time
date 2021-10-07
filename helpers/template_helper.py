from jinja2 import Template
import os
template = Template('''
    <html>
        <head>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=ZCOOL+XiaoWei&display=swap" rel="stylesheet">
        </head>
        <body>
            <div class="story-title"> {{ title }}</div>
            <div class="story-body">
            {% for item in items %}
                <div class="hanzi-container">
                    <div class="hanzi-pinyin">
                        {{ item.pinyin | default("", true) }}
                    </div>
                    <div class="hanzi-title">
                        {{ item.word }}
                    </div>
                </div>
            {% endfor %}
            <div/>
        </body>
        <style>
        html {
            font-family: 'ZCOOL XiaoWei', serif;
            background-color: #747373;
            color: white;
        }
        body {
            padding: 20px;
            font-size: 40px;
        }
        .story-body {
            display: flex;
            flex-wrap: wrap;
            margin-inline: 20%;
        }
        .story-title {
            text-align: center;
            margin-block: 5%;
            font-size: xxx-large;
        }
        .hanzi-container {
            display: flex;
            flex-direction: column;
            border-bottom: 10px solid transparent;
        }
        .hanzi-pinyin {
            color: #ff4d00;
        }
        </style>
    </html>
    ''')

hard_to_read = ['']


def render_template(transciption_file, title):

    with open(transciption_file, "r") as myfile:
        data = [char for char in myfile.readlines()[0]]
        hanzi_items = list(map(lambda x: {'word': x, 'pinyin': ''}, data))
        output = template.render(
            title=title,
            items=hanzi_items
        )
        return output


def write_to_file_and_open(content, filename):
    f = open(f'{filename}.html', "w+")
    f.write(content)
    f.close()
    os.system(f'open {filename}.html')
