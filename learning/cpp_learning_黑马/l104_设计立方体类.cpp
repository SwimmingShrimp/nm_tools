/*
 * @Author: lixialin lixialin@nullmax.ai
 * @Date: 2024-05-09 21:30:15
 * @LastEditors: lixialin lixialin@nullmax.ai
 * @LastEditTime: 2024-05-09 22:12:23
 */
#include<iostream>
using namespace std;



class Cube{
private:
    int length;
    int height;
    int width;
public:
    void set_length(int length_new){
        length=length_new;
    };
    void set_height(int height_new){
        height=height_new;
    };
    void set_width(int width_new){
        width=width_new;
    };
    int get_length(){
        return length;
    };
    int get_height(){
        return height;
    };
    int get_width(){
        return width;
    };
    int area(){
        return 2*(length*height + length*width + height*width);
    };
    int volume(){
        return length*height*width;
    };
    void group_equal(Cube &c){
        if(length==c.get_length() && height==c.get_height() && width==c.get_width()){
            cout << "成员函数判断：两个立方体相等" << endl;
            return;
        };
        cout << "成员函数判断：两个立方体不相等" << endl;
    };
};

void equal(Cube &c1,Cube &c2){
    if (c1.get_height()==c2.get_height() && c1.get_length()==c2.get_length() && c1.get_width()==c2.get_width()){
        cout << "全局函数判断：两个立方体相等" << endl;
    }
    else
    {
        cout << "全局函数判断：两个立方体不相等" << endl;
    };
};

int main(){
    Cube c1;
    c1.set_length(10);
    c1.set_height(5);
    c1.set_width(4);   
    int area1 = c1.area();
    int volume1 = c1.volume();
    cout << "c1立方体的面积为：" << area1 << ";c1立方体的体积为：" << volume1 << endl;
    
    Cube c2;
    c2.set_length(10);
    c2.set_height(5);
    c2.set_width(3);
    int area2 = c2.area();
    int volume2 = c2.volume();
    cout << "c2立方体的面积为：" << area2<< ";c2立方体的体积为：" << volume2 << endl;
    //全局函数判断两个立方体是否相等
    equal(c1,c2);
    //成员函数判断两个立方体是否相等
    c1.group_equal(c2);
    return 0;
}