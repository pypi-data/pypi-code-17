import argumentsprovider
import samplingProvider
import exceptions
import logging
import complexityResolver

def main():
	
	logging.basicConfig(filename="log.txt",level=logging.DEBUG)
	try:
		# Input parameters validation
		args = argumentsprovider.ArgumentsProvider().validate_arguments()
		
		# Sampling algorithm
		samplingResult = samplingProvider.SamplingProvider(args.timeout, args.samplingFrom, args.samplingTo).DoSampling();
		
		# If there is less than 3 points result would be a completely bullshit
		if (len(samplingResult) < 3):
			print ("Sampling didn't gave enough points, can't determine complexity. Try with lower value of samplingFrom")
			return
		
		# Compute complexity
		complexity = complexityResolver.ComplexityResolver.Resolve(samplingResult);
		print ("The complexity of algorithm is most probably: ", complexity)
		
	except exceptions.ArgumentException as err:
		print (err)
	except exceptions.NotImplementedException:
		print ("You didnt implemented algorithm in Algortihm.Execute")
	except Exception as err:
		print ("Something went wrong")
		print (err)
		logging.error(err);
		
if __name__ == "__main__":
    main()