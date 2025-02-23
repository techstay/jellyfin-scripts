prompt = "你是一个数学家，擅长解决数学问题"
message = "数字3.9和3.11哪个大，给出具体推理过程"


def test_deepseek():
    from my_utils.my_ai import deepseek_client

    deepseek_client.chat(
        prompt=prompt,
        message=message,
    )
    deepseek_client.stream_print()


def test_gptdos():
    from my_utils.my_ai import gptdos_client

    gptdos_client.chat(
        prompt=prompt,
        message=message,
    )
    gptdos_client.stream_print()
