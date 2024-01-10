import json
from StatusCodes import StatusCode


class ExecutionHandler:
    @staticmethod
    async def execute_code_asynchronously(function_class, func_params, data, websocket):
        # Directly call the asynchronous method of the class
        # Assuming the method name is 'run_async' and it is a static method
        print("Executing: ", function_class, func_params)

        result = await function_class.run_async(**func_params)
        if result['returncode'] == 0:
            response = {**data,
                        **{
                            "statusCode": StatusCode.EXECUTED_SUCCESSFULLY,
                            "StdOut": result['stdout'],
                            "StdErr": result['stderr'],
                        }
                        }
            print("Successful exec : Sending: ", response)
            await websocket.send(json.dumps(response))
        else:
            response = {**data,
                        **{
                            "statusCode": StatusCode.EXECUTION_ERROR,
                            "StdOut": result['stdout'],
                            "StdErr": result['stderr'],
                        }
                        }
            print("Failed exec : Sending: ", response)
            await websocket.send(json.dumps(response))

        # Return the result
        return result


# Example usage
# async def main():
#     # Assuming TurnMusic is the class and it has a static method 'run_async'
#     result = await ExecutionHandler.execute_code_asynchronously(TurnMusic, {'name': 'Your Favorite Song'})
#     print(result)
#
# if __name__ == '__main__':
#     asyncio.run(main())
