import cv2
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

if __name__ == "__main__":
    cam = cv2.VideoCapture(0)
    total = 0
    doubted = 0
    leaky = 0
    verified = 0
    while cam.isOpened():
        try:
            ret, frame = cv2.imread()
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
                is_leaky_hydrophone = False
                print("Exception", e)
            
            if hydrophone_verification_flag == True:
                leaky +=1
                
                #Going For identification of Leaky Cylinder
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
        
                
            
            
        
        
        
        

            
