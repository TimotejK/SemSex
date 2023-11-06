
if __name__ == '__main__':
    with open('klasifikacija_surovo.txt', 'r') as file:
        lines = file.readlines()

    lines = list(map(lambda x: x.strip(), lines))
    samples = []
    description = None
    for line in lines:
        if line.startswith('•'):
            if description is not None:
                print("Error", line)
            description = line
        elif description is not None:
            # classes
            classes = list(map(lambda x: x.strip(), line.split(',')))
            samples.append((description.replace('•', '').strip(), classes))
            description = None

    print(samples)