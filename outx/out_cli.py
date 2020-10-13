def printOut(records):
    if (len(records) >= 1):
        print(str(len(records)) + ' ' + ('records match' if (len(records) > 1) else 'record matches') + ' your query\n')
        for record in records:
            for key in record:
                print(key + ': ' + str(record[key]))
            print('')
    else:
        print('selection is empty')