import requests
import timeit
import base64

# the top secret key. This is a unique identifier that tells Google who is accessing the API
key = "AIzaSyAYhg5B10ji-Dv0FglIg-Xx3LDx8pOyoRk"

# the API wants the image to be encoded in a special format. This function converts your image to the special format.
# Don't worry about this!
def encode_img(image_path):
    f = open(image_path)
    return f.read()


def post_image(image_path, num_results):
    img_string = encode_img(image_path)
    payload = {
        "requests": [
            {
                "image": {
                    "content": img_string
                },
                "features": [
                    {
                        "type": "LABEL_DETECTION",
                        "maxResults": num_results
                    }
                ]
            }
        ]
    }

    r = requests.post("https://vision.googleapis.com/v1/images:annotate?key=" + key, json=payload)
    if r.status_code == 200:
        return r.json()
    else:
        print(r.json())


def parse_labels(json_response):
    #print(json_response)
    try:
        response_obj = json_response["responses"][0]["labelAnnotations"]
        labels = []
        for annotation in response_obj:
            labels.append(annotation["description"])
        return labels
    except KeyError:
        print("Error: " + str(json_response))
        exit(0)


def is_stop_sign(file_path, num_responses=10):
    response = post_image(file_path, num_responses)
    labels = parse_labels(response)
    found = False
    for tag in labels:
        if tag.lower() == "stop sign":
            found = True
    return found

if __name__ == "__main__":
    start = timeit.default_timer()
    print(is_stop_sign("../images/stopsign.txt"))
    end = timeit.default_timer()
    print("Time elapsed: " + str(round((end - start) * 1000)) + " ms")
