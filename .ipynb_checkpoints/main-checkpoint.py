def main():
    from linebot.v3.messaging import Configuration, MessagingApi, ApiClient, PushMessageRequest, ApiException


configuration = Configuration(
    access_token = 'DMg8NmxI9n9UM7d7k21uBYt5cg2bbhrp7diPgN8ZE5hUypMo90HWKDSvHstK7Fy+NjwK+rWY9nXDKTlsSM+ofeck4EggqxcQXlBoMojXKjot/fUM3qv7iJLEpzozMC1/3ud304szgER1ynYXrW3+ygdB04t89/1O/w1cDnyilFU='
)

message_dict = {
    'to': 'U883c49cc92f1e0a1b2de45aefafd3886',
    'messages': [
        {
            'type': 'text',
            'text': 'テストメッセージ'
        },
    ]
}

with ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = MessagingApi(api_client)
    push_message_request = PushMessageRequest.from_dict(message_dict)

    try:
        push_message_result = api_instance.push_message_with_http_info(push_message_request, _return_http_data_only=False)
        print(f'The response of MessagingApi->push_message status code => {push_message_result.status_code}')
    except ApiException as e:
        print('Exception when calling MessagingApi->push_message: %s\n' % e)
        
if __name__ == "__main__":
    main()