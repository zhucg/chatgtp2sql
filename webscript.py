from flask import  Flask,render_template,request
from openai import OpenAI
import json
import pymysql
from tabulate import tabulate
app=Flask(__name__)

@app.route('/')
def start():
@app.route('/result' ,methods=["POST","GET"])
def result():
    client = OpenAI(
        api_key="sk-XXXXXXXXXXXXXXXXXXXXXXXXXX",
    )
    if request.method=='GET':
        input_text  = request.args.get('description', '')
    else:
        result = request.form
        # 用户输入
        input_text = result["description"]
    prompt = f"""
    The database table is as follows: CREATE TABLE print_record (
    id int NOT NULL AUTO_INCREMENT, -- Unique ID for each record
    device varchar(45), --Device Name of the record
    created_at timestamp,
    updated_at timestamp,
    file_name varchar(255),
    total_slice int ,
    thickness decimal(6,2),
    material varchar(145),
    duration varchar(145),
    status int,
    printed_times int,
    current_layer int,
    intensity int,
    exposure_time int,
    finish_time varchar(100),
    job_id varchar(45),
    start_time varchar(45),
    record_id varchar(45),
    source varchar(45),
    weight varchar(45),
    support_weight varchar(45),
    volume varchar(45),
    timezone varchar(45),
    work_id varchar(45),
    )

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt.strip(),
        max_tokens=512,
        temperature=0,
        #stream=True
    )
    return model_list(response.choices)
    #for chunk in response:
    #    print(chunk.choices[0].text, end='')
    #    return chunk.choices[0]
def model_list(result):
    list = []
    for row in result:
        dict = {}
        for k, v in row.__dict__.items():
            if not k.startswith('_sa_instance_state'):
                dict[k] = v
    list.append(dict)
    lines = result[0].text.split('\n')
    for line in lines:
        print(line)
    text = ""
    for line in lines:
        if line.strip().startswith('SELECT') and line.strip().endswith(';'):
            text = line.strip()
            break
        elif line.strip().startswith('SELECT') and not line.strip().endswith(';'):
            text = " " + line.strip()
        elif line.strip().endswith(';'):
            text += " " + line.strip()
            break
        else:
            text += " " + line.strip()
        #if line.strip().startswith('SELECT'):
        #    text = line.strip()
        #    print(text)
        #    break
    res = run_sql(text)
    return "The generated SQL is : " + text + "<br><br>The result of execution is:<br>" + res
    return text
def run_sql(sql):
    try:
        db=pymysql.connect(host='localhost',user='db_user',password='db_password',port=3306,db='db_name')
        cur=db.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        return tabulate(results, headers="", tablefmt="html")
    except Exception as e:
        return "err:" + sql


if __name__=="__main__":
    #app.logger.setLevel(logging.DEBUG)
    app.run(port=80,host="127.0.0.1",debug=True)
