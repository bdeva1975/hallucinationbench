from hallucinationbench import score

context = """
The Eiffel Tower is located in Paris, France. It was constructed between
1887 and 1889 as the entrance arch for the 1889 World's Fair. The tower
is 330 metres tall and is the most visited monument in the world.
"""

response = """
The Eiffel Tower is in Paris. It was built in 1889 and stands 330 metres
tall. It was designed by Leonardo da Vinci and attracts over 7 million
visitors every year.
"""

result = score(context=context, response=response)
print(result)