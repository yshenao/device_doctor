from application.apps.testpoint.db.dal import DBProxy


def main(cronjob_id1, cronjob_id2):
    diff_1 = DBProxy().get_testpoint_abnormal_analysis(-1, -1, cronjob_id1)
    diff_2 = DBProxy().get_testpoint_abnormal_analysis(-1, -1, cronjob_id2)
    map_1, map_2 = {}, {}
    for r1 in diff_1:
        map_1[r1.testpoint_id] = r1.result
    for r2 in diff_2:
        map_2[r2.testpoint_id] = r2.result

    equal, diff = 0, 0
    for id, r1 in map_1.items():
        if map_2[id] == r1:
            equal += 1
        else:
            diff += 1
    all = equal + diff
    print('诊断结果相同的数量为{}，不同的数量为{}'.format(equal, diff))
    print('报警准确率{}%提升至{}'.format(equal * 100 / all, 100))


if __name__ == '__main__':
    main(24, 33)
