class ExecutionHandler:

    @staticmethod
    async def execute_code_asynchronously(function_class, func_params):
        # Directly call the asynchronous method of the class
        # Assuming the method name is 'run_async' and it is a static method
        result = await function_class.run_async(**func_params)

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
