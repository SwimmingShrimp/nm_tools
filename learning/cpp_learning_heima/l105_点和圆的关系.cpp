#include<iostream>
using namespace std;

class Point{
public:
    void setX(int x1){
        x = x1;
    };
    void setY(int y1){
        y = y1;
    };
    int getX(){
        return x;
    };
    int getY(){
        return y;
    };
private:
    int x;
    int y;
};

class Circle{
public:
    void setR(int r1){
        r = r1;
    };
    int getR(){
        return r;
    };
    void setCenter(Point center1){
        m_center = center1;
    };
    Point getCenter(){
        return m_center;
    };

private:
    int r;
    // 在类中，可以让另一个类，作为本类的成员
    Point m_center;
};



void judge(Circle &c,Point &p){
    int cx = c.getCenter().getX();
    int cy = c.getCenter().getY();
    int cr = c.getR();
    int px = p.getX();
    int py = p.getY();
    int distance1 = (cx-px)*(cx-px) + (cy-py)*(cy-py);
    int distance2 = cr*cr;
    if(distance1==distance2){
        cout << "点在圆上" << endl;
    }
    else if(distance1<distance2){
        cout << "点在圆内" << endl;
    }
    else{
        cout << "点在圆外" << endl;
    };
};

int main(){
    Circle c;
    c.setR(10);
    Point center;
    center.setX(0);
    center.setY(0);
    c.setCenter(center);
    Point p;
    p.setX(0);
    p.setY(11);
    judge(c,p);   
    return 0;
};