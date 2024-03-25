from fastapi import FastAPI
import pymysql
import cv2
import numpy as np
import os

app = FastAPI()

def connect_to_db():
    return pymysql.connect(
        host="3.27.125.190",
        port=3306,
        user="admin",
        password="entertainment_admin",
        database="entertainment_db",
    )

def video_gen(act_topic,dialogues):
    
    # Directory to save the video
    output_dir = './content'

    # Video properties
    frame_width = 1920
    frame_height = 1080
    fps = 30

    # Texts to display
    texts = [act_topic]
    for dialogue in dialogues:
        str_list = [dialogue["character"],": ", dialogue["line"]]
        con_dialogue = "".join(str_list)
        #texts = np.concatenate(texts,dialogue.)
        texts.append(con_dialogue)  # Add your texts here

    # Font properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = (255, 255, 255)  # White color

    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(os.path.join(output_dir, 'output_video.mp4'), fourcc, fps, (frame_width, frame_height))

    # Generate frames with text
    for text in texts:
        # Create a black background
        # Generate a blue background frame
        frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        frame[ :, :, 2] = np.ones([frame_height, frame_width])*25
        frame[ :, :, 1] = np.ones([frame_height, frame_width])*25
        frame[ :, :, 0] = np.ones([frame_height,frame_width])*112 

        # Get text size and position
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        segments = [text[i:i+100] for i in range(0, len(text), 100)]
        #text_x = int((frame_width - text_size[0]))
        #text_y = int((frame_height + text_size[1]))
        text_x = 150
        text_y = 200
        for segment in segments:
            cv2.putText(frame, segment, (text_x,text_y),font, font_scale, font_color, font_thickness, cv2.LINE_AA)
            text_y += 30

        # Put text on the frame
        #cv2.putText(frame, text, (text_x, text_y), font, font_scale, font_color, font_thickness, cv2.LINE_AA)

        # Write frame to video
        for n in range(150):
          video.write(frame)
      

    # Release VideoWriter object
    video.release()
    


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/contents/{content_id}")
async def read_content(content_id:int):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM content WHERE id = %s"
            cursor.execute(sql, (content_id,))
            result = cursor.fetchone()
            if result:
                #return{"content":result}
                act_topic = "Snow White navigates the ominous forest and finds comfort among woodland creatures. She discovers a refuge in the dwarfs' cottage and earns their trust."
                #act_topic = "Snow White"
                dialogue = [
                      {
                            "character": "Snow White",
                            "line": "Oh, what a frightful place this is. I must find shelter before nightfall.",
                      },
                      {
                            "character": "Narrator",
                            "line": "As Snow White ventures deeper into the forest, she stumbles upon a family of rabbits huddled together.",
                      },
                      {
                            "character": "Snow White",
                            "line": "Hello, little ones. I mean you no harm. I'm lost and afraid. Can you help me find a safe place?",
                      }
                ]
                video_gen(act_topic,dialogue)
                return{"messate":"ok"}
            else:
                return{"message":"not found"}
    finally:
        connection.close()
    