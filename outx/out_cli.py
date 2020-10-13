def printOut(records):
    outFileHandler = open('selection.txt', 'w')

    if (len(records) >= 1):
        print(str(len(records)) + ' ' + ('records match' if (len(records) > 1) else 'record matches') + ' your query\n')
        outFileHandler.write(str(len(records)) + ' ' + ('records match' if (len(records) > 1) else 'record matches') + ' your query\n\n')

        for record in records:
            for key in record:
                print(key + ': ' + str(record[key]))
                outFileHandler.write(key + ': ' + str(record[key]) + '\n')
            print('')
            outFileHandler.write('\n')

    else:
        print('selection is empty')

    outFileHandler.close()
