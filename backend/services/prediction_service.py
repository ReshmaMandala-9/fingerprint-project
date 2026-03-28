from ml.predictor import predict_for_user, predict_for_researcher

def predict_user_service(image_path):

    result = predict_for_user(image_path)

    return result


def predict_researcher_service(image_path):

    results = predict_for_researcher(image_path)

    return results