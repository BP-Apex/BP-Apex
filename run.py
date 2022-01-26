import csv
import os
import subprocess
from shutil import copyfile, rmtree
import argparse
import json

BENCHMARK = ['ALEXTASK', 'ANKTRAIN', 'CHEFAPAR', 'CHRL4', 'DISHOWN', 'ENTEXAM', 'KOL16B', 'NOTINCOM', 'RGAME', 'TRISQ']

BENCHMARK_DIR = 'benchmarks'
CORRECT_DIR = os.path.join(BENCHMARK_DIR, "c")
WRONG_DIR = os.path.join(BENCHMARK_DIR, "w")
MARK_DIR = os.path.join(BENCHMARK_DIR, "marks")
TESTCASE_DIR = os.path.join(BENCHMARK_DIR, "testcases")
CSYMB_DIR = os.path.join(BENCHMARK_DIR, "c_symbs")
WSYMB_DIR = os.path.join(BENCHMARK_DIR, "w_symbs")
RESULT_DIR = 'results'

opts = ["bpapex","iter_1","iter_2","iter_4", "dis_0", "dis_1", "fs", "fcd","fdd","fl","fd"]

def parsing_arguments():
  parser = argparse.ArgumentParser(description = "This script is written for the evaluation of BP-Apex")

  parser.add_argument("-option", type = str, default = "bpapex",
    choices = opts + ["all"]
    )
  args = parser.parse_args()
  return args.option

def execute_command(command):
  p = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
  try:
    out, err = p.communicate(timeout=1000000)
    out = out.decode()
    return (out, err)
  except subprocess.TimeoutExpired:
    p.terminate()
    p.wait()
    return ("", True)

def run(opt):
    if not os.path.exists(RESULT_DIR):
        os.mkdir(RESULT_DIR)

    result_opt = os.path.join(RESULT_DIR, opt)
    if not os.path.exists(result_opt):
        os.mkdir(result_opt)

    for benchmark in BENCHMARK:
        result_bench = os.path.join(result_opt, benchmark)

        if not os.path.exists(result_bench):
            os.mkdir(result_bench)

        wrong_dir = os.path.join(WRONG_DIR,benchmark)
        correct_dir = os.path.join(CORRECT_DIR,benchmark)
        mark_dir = os.path.join(MARK_DIR,benchmark)
        wrongs = os.listdir(wrong_dir)
        target_dir = os.path.join(result_opt, benchmark)
        target_c_symb_dir = os.path.join(CSYMB_DIR, benchmark)
        target_w_symb_dir = os.path.join(WSYMB_DIR, benchmark)

        for w in wrongs:

            command = 'python3 bp_apex feedback'

            wrong = os.path.join(wrong_dir, w)
            print('run BP-Apex on ' + wrong + ' --option ' + opt)

            correct = os.path.join(correct_dir, w)
            mark = os.path.join(mark_dir, w.split('.')[0] + '_mark')
            input = os.path.join(TESTCASE_DIR,benchmark+'_testcases')
            c_symb = os.path.join(target_c_symb_dir, w.split('.')[0] + '_symb')
            w_symb = os.path.join(target_w_symb_dir, w.split('.')[0] + '_symb')

            command += ' ' + input
            command += ' ' + wrong
            command += ' ' + correct
            command += ' --mark ' + mark
            command += ' --option ' + opt
            command += ' -symb'
            command += ' --sw ' + w_symb
            command += ' --sc ' + c_symb
            print(command)
            execute_command(command)
            target_res = os.path.join(target_dir, w.split('.')[0] + '_res')

            res = os.path.join('tmp', 'res.json')
            if os.path.exists(res):
                copyfile(res, target_res)
                rmtree('tmp')

def dig(opt):
    headers = ['benchmark','loc_wrong','loc_correct','symb_wrong','symb_correct','matches','time','precision','recall','f1']

    result_opt = os.path.join(RESULT_DIR, opt)
    results_of_benchmark = []
    for benchmark in BENCHMARK:
        row = [benchmark]
        result_bench = os.path.join(result_opt, benchmark)
        results = os.listdir(result_bench)

        sw = 0
        sc = 0
        align = 0
        time = 0
        pre = 0
        rec = 0
        fs = 0
        locw = 0
        locc = 0

        len_of_results = len(results)
        if len_of_results == 0:
            results_of_benchmark.append(row)
            continue

        for result in results:
            result_path = os.path.join(result_bench, result)

            with open(result_path, 'r') as load_f:
                load_dict = json.load(load_f)
                locw += load_dict['loc_wrong']
                locc += load_dict['loc_correct']
                sw += load_dict['symb_wrong']
                sc += load_dict['symb_correct']
                align += len(load_dict['alignment'])
                time += load_dict['time']
                pre += load_dict['precision']
                rec += load_dict['recall']
                fs += load_dict['f_score']

        row.append(int(locw/len_of_results))
        row.append(int(locc/len_of_results))
        row.append(int(sw/len_of_results))
        row.append(int(sc/len_of_results))
        row.append(int(align/len_of_results))
        time_str = '%.2f' % (time/len_of_results)
        row.append(time_str)
        pre_str = '%.2f' % (pre/len_of_results)
        row.append(pre_str)
        rec_str = '%.2f' % (rec/len_of_results)
        row.append(rec_str)
        f1_str = '%.2f' % (fs/len_of_results)
        row.append(f1_str)

        results_of_benchmark.append(row)

    result_csv = os.path.join(result_opt, 'result.csv')
    with open(result_csv,'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(results_of_benchmark)

def get_rows(path):
    res = []
    with open(path) as doc:
        reader = csv.reader(doc)
        header = next(reader)
        for row in reader:
            res.append(row)
    return res

def rq1():
    apex_path = os.path.join(RESULT_DIR, 'apex.csv')
    bpapex_path = os.path.join(RESULT_DIR, 'bpapex', 'result.csv')

    if os.path.exists(apex_path) and os.path.exists(bpapex_path):

        apex = get_rows(apex_path)
        bpapex = get_rows(bpapex_path)
        line = 0
        rq1 = []
        headers = ['benchmark', 'matches/apex', 'matches/bpapex', 'time/apex', 'time/bpapex',
                   'precision/apex','precision/bpapex', 'recall/apex', 'recall/bpapex', 'f1/apex', 'f1/bpapex']

        for benchmark in BENCHMARK:
            row = []
            row.append(apex[line][0]) # benchmark

            matched_apex = apex[line][5]
            row.append(matched_apex) # matched/apex

            matched_bpapex = bpapex[line][5]
            row.append(matched_bpapex) # matched/bpapex

            time_apex = apex[line][6]
            row.append(time_apex) # time/apex

            time_bpapex = bpapex[line][6]
            row.append(time_bpapex) # time/bpapex

            precision_apex = apex[line][7]
            row.append(precision_apex) # precision/apex

            precision_bpapex = bpapex[line][7]
            row.append(precision_bpapex) # precision/bpapex

            recall_apex = apex[line][8]
            row.append(recall_apex) # recall/apex

            recall_bpapex = bpapex[line][8]
            row.append(recall_bpapex) # recall/bpapex

            fscore_apex = apex[line][9]
            row.append(fscore_apex) # fscore/apex
            fscore_bpapex = bpapex[line][9]
            row.append(fscore_bpapex) # fscore/bpapex
            rq1.append(row)
            line += 1

        get_average(headers, rq1, 1)
        rq1_csv = os.path.join(RESULT_DIR, 'rq1.csv')
        with open(rq1_csv, 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(rq1)

def get_average(headers, rq, begin):
    average = []
    average.append('AVERAGE')

    for i in range(1, begin):
        valleft = 0
        valright = 0
        for row in rq:
            [left, right] = row[i].split('/')
            valleft += int(left)
            valright += int(right)
        average.append(str(valleft) + '/' + str(valright))

    for i in range(1, begin):
        [left, right] = average[i].split('/')
        averleft = int(left) / len(BENCHMARK)
        averright = int(right) / len(BENCHMARK)
        average[i] = str(averleft) + '/' + str(averright)

    for i in range(begin, len(headers)):
        val = 0
        for row in rq:
            val += float(row[i])
        average.append(val)

    for i in range(begin, len(average)):
        average[i] = '%.2f' % (average[i] / len(BENCHMARK))

    rq.append(average)

def rq2():
    opts = ["bpapex", "dis_0", "dis_1", "iter_1", "iter_2", "iter_4","apex"]
    rq2 = {}
    times = {}
    precision = {}
    recall = {}
    fs = {}

    for opt in opts:
        if opt == 'apex':
            result = os.path.join(RESULT_DIR, 'apex.csv')
        else:
            result = os.path.join(RESULT_DIR, opt, 'result.csv')
        assert os.path.exists(result)
        res = []
        with open(result) as doc:
            reader = csv.reader(doc)
            header = next(reader)
            for row in reader:
                res.append(row)

        index = 0
        for benchmark in BENCHMARK:
            assert res[index][0] == benchmark
            try:
                times[opt].append(float(res[index][6]))
            except:
                times[opt] = [float(res[index][6])]

            try:
                precision[opt].append(float(res[index][7]))
            except:
                precision[opt] = [float(res[index][7])]

            try:
                recall[opt].append(float(res[index][8]))
            except:
                recall[opt] = [float(res[index][8])]

            try:
                fs[opt].append(float(res[index][9]))
            except:
                fs[opt] = [float(res[index][9])]

            index += 1

        fs[opt] = str(fs[opt])
        precision[opt] = str(precision[opt])
        times[opt] = str(times[opt])
        recall[opt] = str(recall[opt])

    rq2['time'] = times
    rq2['precision'] = precision
    rq2['recall'] = recall
    rq2['fs'] = fs

    with open(os.path.join(RESULT_DIR, 'rq2.json'), "w") as f:
        json.dump(rq2, f, indent= 2, separators=(', ', ': '))

    plot(rq2)

def plot(rq):
    metrics = ['time', 'fs']
    opts = ["bpapex", "dis_0", "dis_1", "iter_1", "iter_2", "iter_4","apex"]

    metric_dict = {}
    metric_dict['time'] = 'Time(s)'
    metric_dict['fs'] = r'F$_1$ Score'


    opt_dict = {}
    opt_dict['bpapex'] = 'BP-Apex'
    opt_dict['dis_0'] = r'threshold$_0$, iter$_3$'
    opt_dict['dis_1'] = r'threshold$_1$, iter$_3$'

    opt_dict['iter_1'] = r'iter$_1$'
    opt_dict['iter_2'] = r'iter$_2$'
    opt_dict['iter_4'] = r'iter$_4$'
    opt_dict['apex'] = 'Apex'

    line_dict = {}
    line_dict['bpapex'] = 'ro-'
    line_dict['dis_0'] = 'g+--'
    line_dict['dis_1'] = 'b^--'

    line_dict['iter_1'] = 'y|--'
    line_dict['iter_2'] = 'c<--'
    line_dict['iter_4'] = 'm>--'

    for metric in metrics:
        import matplotlib.pyplot as plt

        res_metric = rq[metric]
        x = [1,2,3,4,5,6,7,8,9,10]
        for opt in opts:
            y = eval(res_metric[opt])
            y =sorted(y)

            if opt != 'apex':
                plt.plot(x, y, line_dict[opt], label=opt_dict[opt])
            else:
                plt.plot(x, y, label=opt_dict[opt],color='mediumslateblue', linestyle='--', marker='o')

        plt.xlabel('submissions')
        plt.ylabel(metric_dict[metric])
        plt.legend()
        path = os.path.join(RESULT_DIR, metric + '.pdf')
        plt.savefig(path)
        plt.clf()

def rq3():
    opts = ["bpapex","fs", "fcd", "fdd", "fd", "fl"]
    rq3 = []
    headers = ['benchmark', 'BP-Apex', '-fs', '-fcd', '-fdd', '-fd', '-fl']
    line = 0
    for benchmark in BENCHMARK:
        row = [benchmark]
        for opt in opts:
            path = os.path.join(RESULT_DIR, opt, 'result.csv')
            res = get_rows(path)
            fs = res[line][-1]
            row.append(fs)
        rq3.append(row)
        line += 1

    get_average(headers, rq3, 1)

    rq3_csv = os.path.join(RESULT_DIR, 'rq3.csv')
    with open(rq3_csv, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rq3)

def benchmark():
    apex_path = os.path.join(RESULT_DIR, 'apex.csv')
    apex = get_rows(apex_path)
    bpapex_path = os.path.join(RESULT_DIR, 'bpapex', 'result.csv')
    bpapex = get_rows(bpapex_path)
    mark_path = os.path.join(BENCHMARK_DIR, 'marks')

    headers = ['benchmark','numbers', 'loc/buggy', 'loc/correct', 'sym expr/buggy', 'sym expr/correct', 'marks']
    line = 0
    benchmarks = []
    for benchmark in BENCHMARK:
        row = []
        row.append(apex[line][0])  # benchmark
        path = os.path.join(mark_path, benchmark)

        marks = os.listdir(path)
        row.append(len(marks))

        loc_wrong = bpapex[line][1]
        loc_correct = bpapex[line][2]
        row.append(loc_wrong)  # loc
        row.append(loc_correct)

        symb_wrong = bpapex[line][3]
        symb_correct = bpapex[line][4]
        row.append(symb_wrong)
        row.append(symb_correct)

        nums = 0
        for file in marks:
            mark = os.path.join(path, file)
            if os.path.exists(mark):
                f = open(mark, 'r')
                res = f.readlines()
                if len(res) > 0:
                    nums += len(eval(res[0]))
        nums /= len(marks)
        row.append(int(nums))
        line += 1
        benchmarks.append(row)
    benchmark_csv = os.path.join(RESULT_DIR, 'benchmark.csv')
    with open(benchmark_csv, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(benchmarks)

def main():
    opt = parsing_arguments()

    if opt == 'all':
        for opt in opts:
            run(opt)
            dig(opt)
        benchmark()
        rq1()
        rq2()
        rq3()
    else:
        run(opt)
        dig(opt)


if __name__ == '__main__':
    main()
