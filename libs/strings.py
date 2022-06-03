messages = {
        "NOT_FOUND": "{} not found",
        "ERROR_DELETING": "error while deleting from database",
        "ALREADY_TAKEN": "{} already exists",
        "CREATED_SUCCESSFULLY": "{} created successfuly",
        "ERROR_ADDING": "error while adding to database",
        "CANT_INPUT_NEGATIVE": "price is negative, please insert positive",
        "ERROR_CREATING_PRODUCT": "error ouccerd while creating product",
        "INVALID_INPUTS": "wrong username or password",
        "DONE_MODIFICATIONS": "all modifications are made",
        "ALREADY_RATED": "you've already rated this product",
        "CONFIRMATION_EXPIRED": "confrimation expired",
        "RESEND_SUCCESSFUL": "resend successful",
        "RESEND_FAILED": "resend failed",
        "SENT_CONFIRMATION_MAIL": "a confirmation email has been sent to you, check it out",
        "ACCOUNT_NOT_ACTIVE": "account is not activated, please check your inbox",
        "ILLIGAL_FILENAME": "illegal filename",
        "DELETED_SUCCESSFULLY": "{} deleted successfully",
        "IMAGE_UPLOADED": "image uploaded, basename: {}",
        "EXTENSION_NOT_ALLOWED": "extension {} is not allowed",
        
}



def get_text(msg):
    return messages[msg]
