#include<iostream>
using namespace std;
#include<string>
#include<unistd.h>

// 创建英雄结构体
struct Hero{
    string name;
    int age;
    string sex;
};
void sortHero(struct Hero hArray[],int len){
    for(int i=0;i<len;i++){
        for(int j=0;j<i;j++){
            if(hArray[i].age < hArray[j].age){
                struct Hero temp = hArray[i];
                hArray[i] = hArray[j];
                hArray[j] = temp;
            };
        };
    };
    cout << "根据年龄排序后的英雄列表" << endl;
    for(int i=0;i<len;i++){
        cout << "姓名：" << hArray[i].name << "\t年龄：" << hArray[i].age << "\t性别：" << hArray[i].sex << endl;
    };
    
};

int main(){
    // 创建英雄结构体数组
    struct Hero hArray[5]={{"刘备",23,"男"},{"关羽",22,"男"},{"张飞",20,"男"},{"赵云",21,"男"},{"貂蝉",19,"女"}};
    // 根据英雄年龄进行排序
    int len = sizeof(hArray)/sizeof(hArray[0]);
    sortHero(hArray,len);

    pause();
    return 0;
}
