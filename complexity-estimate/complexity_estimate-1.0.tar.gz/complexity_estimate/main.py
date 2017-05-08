import random
from complexity_estimate.UsageException import UsageException
from complexity_estimate.ComplexCalc import ComplexCalc
from complexity_estimate.Algorythms import example_logn, example_n, \
    example_nlogn, example_nn, example_nnn


def main():
    try:
        tab = [10000 * random.random() for _ in range(int(pow(2, 16)))]
        c1 = ComplexCalc(example_logn, tab, 2, 1, 16, 30)
        print("\nExampleLOGN: ")
        c1.calculate_complexity()
        tmp = c1.get_time_foreseer()(100000)
        c1.get_size_foreseer()(tmp)

        tab = [10000 * random.random() for _ in range(int(pow(2, 14)))]
        c2 = ComplexCalc(example_n, tab, 2, 1, 14, 30)
        print("\nExampleN: ")
        c2.calculate_complexity()
        tmp = c2.get_time_foreseer()(100000)
        c2.get_size_foreseer()(tmp)

        tab = [10000 * random.random() for _ in range(int(pow(2, 12)))]
        c3 = ComplexCalc(example_nlogn, tab, 2, 5, 12, 30)
        print("\nExampleNLOGN: ")
        c3.calculate_complexity()
        tmp = c3.get_time_foreseer()(1000000000)
        c3.get_size_foreseer()(tmp)

        tab = [10000 * random.random() for _ in range(int(pow(2, 10)))]
        c4 = ComplexCalc(example_nn, tab, 2, 1, 10, 30)
        print("\nExampleNN: ")
        c4.calculate_complexity()
        tmp = c4.get_time_foreseer()(100000)
        c4.get_size_foreseer()(tmp)

        tab = [10000 * random.random() for _ in range(int(pow(2, 8)))]
        c5 = ComplexCalc(example_nnn, tab, 2, 1, 8, 60)
        print("\nExampleNNN: ")
        c5.calculate_complexity()
        tmp = c5.get_time_foreseer()(100000)
        c5.get_size_foreseer()(tmp)

    except UsageException as e:
        print("Wrong usage: ", e)
        exit(-1)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
