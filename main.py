import cv2
import os
import numpy as np
def leak_detection(image):
    global total
    print("Leak detection started")
    return True
def hydrophone_verification():
    print("Verifying using Hydrophone")
    return True
def identify_leaky_cylinder():
    print("identifying leaky cylinder")
    return 1

def add_logo(image, logo, pos_y, pos_x):
     # Add the logo image to the video frame
    if isinstance(image, str) and os.path.exists(image):
        image = cv2.imread(image)
    if isinstance(logo, str) and os.path.exists(logo):
        logo = cv2.imread(logo)
        print(logo)
    # Read logo and resize
    size = 70
    logo = cv2.resize(logo, (size, size))
    # Create a mask of logo
    img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
    # Set ROI for logo placement
    roi = image[10:size+10, 10:size+10]
  
    # Set an index of where the mask is
    roi[np.where(mask)] = 0
    roi += logo
     
    # alpha = 0.5
    # beta = 1 - alpha
    # overlay = cv2.addWeighted(image[pos_y:pos_y+logo.shape[0], pos_x:pos_x+logo.shape[1]], alpha, logo, beta, 0)
    # image[pos_y:pos_y+logo.shape[0], pos_x:pos_x+logo.shape[1]] = overlay
    return image

def put_data_on_image(image, total, doubted, leaky, verified):
    
    if isinstance(image, str) and os.path.exists(image):
        image = cv2.imread(image)
    else:
        text1 = f" Total: {total}"
        text2 = f" Doubted: {doubted}"
        text3 = f" Leaky: {leaky}"
        text4 = f" Verification: {verified}"
        heading = "Automatic Leak Detection"
        
        base_x = 950
        base_y = 450
        
        #Rectangele Behind Headings
        cv2.rectangle(image, (0, 0),(1550, 80),(250,255,208), thickness=-1 )
        #Heading
        cv2.putText(image, heading, (280,50), cv2.FONT_HERSHEY_COMPLEX, 1.8, (0,0,0), thickness=2)
        image = add_logo(image, "Bharat-Petroleum-logo.png", 20,20)
        
        
        #Data Rectangle
        cv2.rectangle(image, (base_x+10, base_y-140),(base_x + 350, base_y+180),(255,253,208), thickness=-1 )
      
        cv2.putText(image, "Auto", (base_x+100,base_y-80), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,255), thickness=2)
        
        cv2.putText(image, text1, (base_x,base_y), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), thickness=2)
        cv2.putText(image, text2, (base_x,base_y + 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), thickness=2)
        cv2.putText(image, text3, (base_x,base_y + 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), thickness=2)
        cv2.putText(image, text4, (base_x,base_y + 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), thickness=2)
        return image
        
        
    

if __name__ == "__main__":
    cam = cv2.VideoCapture("Data\plant.mp4")
    total = 0
    doubted = 0
    leaky = 0
    verified = 0
    while cam.isOpened():
        try:
            ret, frame =cam.read()
        except Exception as e:
            ret = None
            frame = None
            print("Exception", e)
        if ret == False or frame is None:
            print("Camera Frame cannot be loaded")
            break
        
        try:
            is_leaky = leak_detection(frame)
        except Exception as e:
            is_leaky = False
            print("Exception", e)
        
        if is_leaky == True:
            doubted +=1
            
            #Going for Hydrophone verfication
            try:
                hydrophone_verification_flag = hydrophone_verification()
                verified +=1
            except Exception as e:
                hydrophone_verification_flag = False
                print("Exception", e)
            
            if hydrophone_verification_flag == True:
                leaky +=1
                
                frame = put_data_on_image(frame,total, doubted, leaky, verified)
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
        
                
            
            
        
        
        
        

            
