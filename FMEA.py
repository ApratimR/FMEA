from FNNH import FNNH
import base64

char_array="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

def FMEA(data="",password="",mode=1,blocksize=64,stress=1):
    print(type(data))
    print(data,password,mode,blocksize,stress)



    password = password.encode(encoding="UTF-8")
    password = base64.urlsafe_b64encode(password)
    password = password.decode(encoding="UTF-8")
    password = password.replace("=","")
    password = FNNH(password,blocksize,stress * 64,returnmode="array",maxreturnval = 64)

    if mode == 1: #this is encrypt
        data = data.encode(encoding="UTF-8")
        data = base64.urlsafe_b64encode(data)
        data = data.decode(encoding="UTF-8")
        data = data.replace("=","")

        temp_for_data = []
        for temp in range(len(data)):
            temp_for_data.append(char_array.index(data[temp]))

        password_copy = password[:]
        counter = 0
        seed = 1
        tempdata = []


        for temp in temp_for_data:
            tempdata.append(password_copy[counter]^temp)
            counter+=1
            if counter == blocksize:
                counter = 0
                password_copy = password[:]
                password_copy = list(password_copy)
                password_copy.append(seed)
                password_copy = FNNH(password,blocksize,stress * 64,returnmode="array",maxreturnval = 64)
                seed+=1

        temp_enc_arr_to_str = str()
        for temp in tempdata:
            temp_enc_arr_to_str+=char_array[temp]

        return temp_enc_arr_to_str


#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================


    elif mode == 2: #this is decrypt
        temp_for_data = []
        for temp in range(len(data)):
            temp_for_data.append(char_array.index(data[temp]))

        password_copy = password[:]
        counter = 0
        seed = 1
        tempdata = []

        for temp in temp_for_data:
            tempdata.append(password_copy[counter]^temp)
            counter+=1
            if counter == blocksize:
                counter = 0
                password_copy = password[:]
                password_copy = list(password_copy)
                password_copy.append(seed)
                password_copy = FNNH(password,blocksize,stress * 64,returnmode="array",maxreturnval = 64)
                seed+=1

        temp_enc_arr_to_str = str()
        for temp in tempdata:
            temp_enc_arr_to_str+=char_array[temp]

        ##top pad
        temp_enc_arr_to_str = str(temp_enc_arr_to_str)
        paddingLenght = 4-(len(temp_enc_arr_to_str) % 4)
        padding = "="*paddingLenght
        temp_enc_arr_to_str += padding


        temp_enc_arr_to_str = temp_enc_arr_to_str.encode(encoding="UTF-8")
        temp_enc_arr_to_str = base64.urlsafe_b64decode(temp_enc_arr_to_str)
        temp_enc_arr_to_str = temp_enc_arr_to_str.decode(encoding="UTF-8")
        temp_enc_arr_to_str = temp_enc_arr_to_str.replace("=","")


        return temp_enc_arr_to_str
    else:
        raise Exception("Invalid Operation")




def main():
    # password = str(input("Enter the password"))
    # data = str(input("Enter the data"))
    # mode = int(input("enter \n 1 To Encrypt\n 2 To Decrypt"))
    # blocksize = int(input("enter the size of block"))
    # stress = int(input("enter the Instruction Cycle requirment factor (increase processing time)"))

    print(FMEA("apratim","apratim",mode=2,blocksize=64,stress=2))


if __name__ == "__main__":
    main()