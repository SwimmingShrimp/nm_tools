#include<iostream>
#include<unistd.h>
using namespace std;
#include<ctime>

int main(){
    // 添加随机数种子，作用是利用系统时间生成随机数，防止每次随机数都一样
    srand((unsigned int)time(NULL));
    // 1. 系统生成随机数
    int num = rand()%100 +1;
    // 2. 玩家进行猜测
    int val = 0;
    cout << "请输入一个1-100之间的整数：" << endl;
    
    // 3. 判断玩家的猜测
    while(1){
        cin >> val;
        if(val>num){
            cout << "猜大了" << endl;
        }
        else if(val<num){
            cout << "猜小了" << endl;
        }
        else{
            cout << "恭喜你，猜对了" << endl;
            break;
        }
    }
    
    // 猜对，退出游戏
    // 猜错，提示玩家猜大了还是猜小了
    // 玩家可以继续猜测
}