/*
 * @Author: lixialin lixialin@nullmax.ai
 * @Date: 2024-04-11 19:57:07
 * @LastEditors: lixialin lixialin@nullmax.ai
 * @LastEditTime: 2024-04-11 20:46:29
 */
#include<iostream>
using namespace std;
#include<string>
#include<unistd.h>
#include<ctime>

// 定义学生结构体
struct Student{
    string name;
    int score;
};

// 定义老师结构体
struct Teacher{
    string name;
    struct Student sArray[5];
};

void fuzhi(struct Teacher tArray[],int len){
    // 随机数种子
    srand((unsigned int)time(NULL));
    for(int i=0;i<len;i++){
        string nameSeed = "ABCDEF";
        tArray[i].name = "Teacher_" ;
        tArray[i].name += nameSeed[i];
        for(int j=0;j<5;j++){
            int random = rand()%61 + 40;          // rand()%61:表示取0-60之间的随机数
            tArray[i].sArray[j].name = "Student_" ;
            tArray[i].sArray[j].name += nameSeed[j];
            tArray[i].sArray[j].score = random;
        };    
    };
};

void printdata(struct Teacher tArray[],int len){
    

    for(int i=0;i<len;i++){
        cout << "老师的名字是" << tArray[i].name << endl;
        for(int j=0;j<5;j++){
            cout << "\t第" << j << "个学生的名字是：" << tArray[i].sArray[j].name <<", 成绩是：" << tArray[i].sArray[j].score << endl;
        };
    };
};

int main(){
    // 创建老师的对象
    struct Teacher tArray[3];

    // 给老师的对象赋值
    int len = sizeof(tArray)/sizeof(tArray[0]);
    fuzhi(tArray,len);
    
    // 打印所有的数据
    printdata(tArray,len);

    pause();
    return 0;
}