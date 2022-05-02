import streamlit as st
from datetime import datetime
import cv2
import os
import boto3

def write_data_to_excel(k):
    f=open('attendance.csv','a')
    dummy=str(datetime.now())
    dummy=dummy.split(' ')
    f.writelines([k+',',dummy[0]+',',dummy[1].split('.')[0]+'\r\n'])
    f.close()

st.title('Smart Attendance System')
run=st.checkbox('Run Camera')

FRAME_WINDOW=st.image([])
camera=cv2.VideoCapture(0)
student_paths=os.listdir('students/')
client=boto3.client('rekognition')
snsclient=boto3.client('sns')

while run:
    _,frame=camera.read()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    FRAME_WINDOW.image(frame)
    
    cv2.imwrite('test.jpg',frame)
    for i in student_paths:
        imageSource=open('test.jpg','rb')
        imageTarget=open('students/'+i,'rb')
        response=client.compare_faces(SimilarityThreshold=70,SourceImage={'Bytes':imageSource.read()},TargetImage={'Bytes':imageTarget.read()})
        #st.write(response)
        if response['FaceMatches']:
            result=i.split('.jpg')[0]
            st.success('Face Identified as ' + result)
            snsclient.publish(TopicArn='arn:aws:sns:eu-west-1:496667932506:SmartAttendnace',Message='The roll number: ' +result+' attendance recorded at '+str(datetime.now()))
            write_data_to_excel(result)
            run=False
            break
    run=False
    break