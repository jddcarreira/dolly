from AptoideUtils import AptoideUtils

def menu():
    print ("1 - Download All Apps from Repo")
    print ("2 - Upload All Apps to Repo")
    print ("9 - Setup/Clean Configuration Files")
    print ("0 - Exit")
    user_input = raw_input ("Choose an option: ")

    aptoide_utils = AptoideUtils()

    if user_input == "1":
        download = aptoide_utils.download()

    elif user_input == "2":
        user_input_store = raw_input ("Insert your store name: ")
        user_input_token = raw_input ("Insert your store token: ")
        upload = aptoide_utils.upload(user_input_store, user_input_token)

    elif user_input == "9":
        clean = aptoide_utils.clean()

    elif user_input == "0":
        exit()
        
    else:
        menu()

    return

menu()