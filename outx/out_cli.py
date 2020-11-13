def printOut(records):
    with open('selection.txt', 'w') as f:
        if (len(records) >= 1):
            print(str(len(records)) + ' ' + ('records match' if (len(records) > 1) else 'record matches') + ' your query\n')
            f.write(str(len(records)) + ' ' + ('records match' if (len(records) > 1) else 'record matches') + ' your query\n\n')

            for record in records:
                for key in record:
                    print(key + ': ' + str(record[key]))
                    f.write(key + ': ' + str(record[key]) + '\n')
                print('')
                f.write('\n')

        else:
            print('selection is empty')
