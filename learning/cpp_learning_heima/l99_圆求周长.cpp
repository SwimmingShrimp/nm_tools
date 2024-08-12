#include<iostream>
using namespace std;
#include<unistd.h>
#include<string>
class Circle{
    //访问权限
public:
    //属性
    int r;
    //行为
    double calculateZC(){
        return 3.14*r*2;
    }
};

int main(){
    //创建对象，实例化
    Circle c1;
    c1.r = 10;
    cout <<"圆的周长是："<<c1.calculateZC()<<endl;
    pause();
    return 0;
    
}