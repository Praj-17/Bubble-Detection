import cv2
import os
import numpy as np
def leak_detection(image):
    global total
    print("Leak detection started")
    leak = [1,0,0]
    is_leaky = False
    if 1 in leak:
        is_leaky= True
    return leak, is_leaky
def hydrophone_verification():
    print("Verifying using Hydrophone")
    hydrophone_working_status = True
    verification_status = True
    return hydrophone_working_status,  verification_status
def identify_leaky_cylinder():
    print("identifying leaky cylinder")
    leaky_cylinder = [1,1,0]
    return leaky_cylinder

def add_logo(image, logo, pos_y, pos_x, pos_y2=None, pos_x2=None):
    if isinstance(image, str) and os.path.exists(image):
        image = cv2.imread(image)
    if isinstance(logo, str) and os.path.exists(logo):
        logo = cv2.imread(logo)
    size = 70
    logo = cv2.resize(logo, (size, size))
    img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
    roi = image[10:size+10, 10:size+10]
    roi[np.where(mask)] = 0
    roi += logo
    
    if pos_y2 is not None and pos_x2 is not None:
        size = 70
        logo = cv2.resize(logo, (size, size))
        img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
        roi = image[10:size+10, image.shape[1]-80-size+70:image.shape[1]-80+70]
        roi[np.where(mask)] = 0
        roi += logo

         # alpha = 0.5
    # beta = 1 - alpha
    # overlay = cv2.addWeighted(image[pos_y:pos_y+logo.shape[0], pos_x:pos_x+logo.shape[1]], alpha, logo, beta, 0)
    # image[pos_y:pos_y+logo.shape[0], pos_x:pos_x+logo.shape[1]] = overlay
    return image

   

def put_data_on_image(image, total, doubted, leaky, verified,status):
    
    if isinstance(image, str) and os.path.exists(image):
        image = cv2.imread(image)
        
    else:
        text1 = f" Total: {total}"
        text2 = f" Doubted: {doubted}"
        text3 = f" Leaky: {leaky}"
        text4 = f" Verification: {verified}"
        heading = "Automatic Leak Detection"
        
        base_x = 950
        base_y = 380
       
        #Rectangele Behind Headings
        cv2.rectangle(image, (0, 0),(1550, 80),(255,255,255), thickness=-1 )
        #Heading
        cv2.putText(image, heading, (270,58), cv2.FONT_HERSHEY_COMPLEX, 1.8, (0,0,0), thickness=2)

        image = add_logo(image, "bpcl_logo.png", 10,10)
        image = add_logo(image, "bpcl_logo.png", 10,10, 10, image.shape[1]-160)

        
        #Data right hand side box
        cv2.rectangle(image, (base_x+10, base_y-300),(base_x + 350, base_y+350),(133,100,9), thickness=-1 )
      
        cv2.rectangle(image, (base_x+30, base_y-130), (base_x+150, base_y-90), (255, 255, 255), -1)
        cv2.rectangle(image, (base_x+30, base_y-130), (base_x+150, base_y-90), (0, 0, 0), 2)
        cv2.rectangle(image, (base_x+30, base_y-70), (base_x+200, base_y-30), (255, 255, 255), -1)
        cv2.rectangle(image, (base_x+30, base_y-70), (base_x+200, base_y-30), (0, 0, 0), 2)
        cv2.rectangle(image, (base_x+30, base_y-10), (base_x+160, base_y+30), (255, 255, 255), -1)
        cv2.rectangle(image, (base_x+30, base_y-10), (base_x+160, base_y+30), (0, 0, 0), 2)
        cv2.rectangle(image, (base_x+30, base_y+50), (base_x+260, base_y+90), (255, 255, 255), -1)
        cv2.rectangle(image, (base_x+30, base_y+50), (base_x+260, base_y+90), (0, 0, 0), 2)

        cv2.putText(image, "Auto", (base_x+100,base_y-180), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,0), thickness=2)
        cv2.putText(image, text1, (base_x+30,base_y-100), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), thickness=2)
        cv2.putText(image, text2, (base_x+30,base_y-40), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), thickness=2)
        cv2.putText(image, text3, (base_x+30,base_y + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), thickness=2)
        cv2.putText(image, text4, (base_x+25,base_y+80), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), thickness=2)


        #draw the lower left corner box
        box_height = 100
        box_width = 457
        box_thickness = -1
        box_color = (133,100,9)
        
        cv2.rectangle(image, (1, image.shape[0] - box_height - 1), (1 + box_width, image.shape[0] - 1), box_color, thickness=box_thickness)

        text = f'Error status: {status} '
        font_scale = 0.9
        font_thickness = 2
        if status == "No Error":
            text_color = (0, 255, 0)
        else:
            text_color = (255, 0, 0)
        
        cv2.putText(image, text, (30, 650), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, font_thickness)

        return image
        
def error_status(img, text, pos, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(255, 255, 255), thickness=2, error_status=None):
    cv2.putText(img, text, pos, font, font_scale, color, thickness)
    if error_status is not None:
        (text_width, text_height), _ = cv2.getTextSize(error_status, font, font_scale, thickness)
        error_pos = (pos[0], pos[1] + text_height + 10)
        cv2.rectangle(img, error_pos, (error_pos[0] + text_width, error_pos[1] + text_height + 10), color, cv2.FILLED)
        cv2.putText(img, error_status, error_pos, font, font_scale, (0, 0, 0), thickness)
    
    

if __name__ == "__main__":
    cam = cv2.VideoCapture("Data\plant.mp4")
    total = 0
    doubted = 0
    leaky = 0
    verified = 0
    status = "No Error"
    while cam.isOpened():
        try:
            ret, frame =cam.read()
        except Exception as e:
            ret = None
            frame = None
            print("Exception", e)
            status = "Camera Disconnected"
        if ret == False or frame is None:
            print("Camera Frame cannot be loaded")
            # error_status(frame, 'Camera Frame cannot be loaded',(20, 50), error_status='Error')
            status = "Camera Disconnected"
            continue
        
        try:
            leak, is_leaky = leak_detection(frame)
        except Exception as e:
            is_leaky = False
            print("Exception", e)
        
        if is_leaky == True:
            doubted +=1
            
            #Going for Hydrophone verfication
            try:
                hydrophone_working_status,  verification_status = hydrophone_verification()
                if hydrophone_working_status ==False:
                    status = "Hydrophone Disconnected"
                verified +=1
            except Exception as e:
                verification_status = False
                print("Exception", e)
            
            if verification_status == True:
                leaky +=1
                
                frame = put_data_on_image(frame,total, doubted, leaky, verified, status)
                #Going For identification of Leaky Cylinder
                 # Press Q on keyboard to exit
                cv2.imshow("frame", frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                
                try:
                    n = identify_leaky_cylinder()
                except Exception as e:
                    print("Excpetion", e)
                    n = 0
                print("Leaky cylinder at ", n)
            else:
                pass
                
            
            
        else:
            pass #continue the while loop
        
     
