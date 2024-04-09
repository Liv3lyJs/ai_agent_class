from swiplserver import PrologMQI


class DoorOpener:

    def KeyFinder(self, ListeCristaux):
        with PrologMQI() as mqi:
                with mqi.create_thread() as prolog_thread:
                    result = prolog_thread.query("member(X, [first, second, third]).")
                    #print(result)

                with PrologMQI() as mqi_file:
                    with mqi_file.create_thread() as prolog_thread:
                        # Load a prolog file
                        result = prolog_thread.query("consult('DoorOpener.pl').")
                        #print(result)
                        # Query the information in the file
                        result = prolog_thread.query(f"main({ListeCristaux},Index).")
                        #print(result)
                        key = result[0]["Index"]
        print(key)
        return key
#questionList = "['gold', 'red', 'red', 'blue', 'yellow', '', '']"
#keyFinder = DoorOpener()
#key = keyFinder.KeyFinder(questionList)
        