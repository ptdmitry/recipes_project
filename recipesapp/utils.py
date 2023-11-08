def make_cooking_steps_article(cooking_steps: str):
    steps = cooking_steps.split('\n')
    return steps


if __name__ == '__main__':
    with open('../dev-local/cooking_steps_example', 'r') as f:
        text = f.readlines()
    text = ''.join(text)
    text = make_cooking_steps_article(text)
    print(text)
