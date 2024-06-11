#include<iostream>
#include<string>
#include<unistd.h>
using namespace std;
#define MAX 1000

//定义联系人结构体
struct Person{
    string name;
    string sex;
    int age;
    string phone;
    string address;
};
//定义通讯录结构体
struct AddressBook{
    struct Person pArray[MAX];
    int size;
};

void showpage(){int input_value;
    cout << "********************" << endl;
    cout << "****1.添加联系人****" << endl;
    cout << "****2.显示联系人****" << endl;
    cout << "****3.删除联系人****" << endl;
    cout << "****4.查找联系人****" << endl;
    cout << "****5.修改联系人****" << endl;
    cout << "****6.清空联系人****" << endl;
    cout << "****0.退出通讯录****" << endl;
    cout << "********************" << endl;
    };

void addPerson(struct AddressBook * abs){
    // 判断通讯录是否已满
    if(abs->size == MAX){
        cout << "通讯录已满" << endl;
        return;
    }
    else{
        string name;
        cout << "请输入联系人的姓名：" << endl;
        cin >> name;
        abs->pArray[abs->size].name = name;
        string sex;
        cout << "请输入联系人的性别：" << endl;
        cin >> sex;
        abs->pArray[abs->size].sex = sex;
        int age;
        cout << "请输入联系人的年龄：" << endl;
        cin >> age;
        abs->pArray[abs->size].age = age;
        string phone;
        cout << "请输入联系人的电话：" << endl;
        cin >> phone;
        abs->pArray[abs->size].phone = phone;
        string address;
        cout << "请输入联系人的住址：" << endl;
        cin >> address;
        abs->pArray[abs->size].address = address;
        abs->size ++;
        cout << "添加成功！" << endl;
    }
};
void showPerson(struct AddressBook * abs){
    if(abs->size==0){
        cout << "通讯录为空！" << endl;
        return;
    }
    else{
        cout << "通讯录联系人信息：" << endl;
        for(int i=0;i<abs->size;i++){
            cout << "姓名：" << abs->pArray[i].name<< "\t";
            cout << "性别：" << abs->pArray[i].sex << "\t";
            cout << "年龄：" << abs->pArray[i].age << "\t";
            cout << "电话：" << abs->pArray[i].phone<< "\t";
            cout << "住址：" << abs->pArray[i].address <<endl;
        }
    } 
};

int isExist(struct AddressBook * abs,string name){
    for(int i=0;i<abs->size;i++){
        if(abs->pArray[i].name==name){
            return i;
        }
    }
    return -1;
}

void deletePerson(struct AddressBook * abs){
    cout << "请输入要删除的联系人的姓名:" << endl;
    string dName;
    cin >> dName;
    int ret = isExist(abs, dName);
    if(ret==-1){
        cout << "查无此人！" << endl;
    }
    else{
        for(int i=ret;i< abs->size;i++){
            abs->pArray[i] = abs->pArray[i+1];
        }
        abs->size--;
        cout << "删除成功！" << endl;
    }
};

void clearPerson(struct AddressBook * abs){
    for(int i=0;i<abs->size;i++){
        abs->pArray[i].name="";
        abs->pArray[i].sex="";
        abs->pArray[i].age=0;
        abs->pArray[i].phone="";
        abs->pArray[i].address="";
    };
    abs->size =0;
    cout << "清空成功！" << endl;
};

void modifyPerson(struct AddressBook * abs){
    cout << "请输入要修改的联系人姓名：" << endl;
    string mName;
    cin >> mName;
    int ret = isExist(abs, mName);
    if(ret==-1){
        cout << "查无此人！" << endl;
    }
    else{
        string name;
        cout << "请输入联系人的姓名：" << endl;
        cin >> name;
        abs->pArray[ret].name = name;
        string sex;
        cout << "请输入联系人的性别：" << endl;
        cin >> sex;
        abs->pArray[ret].sex = sex;
        int age;
        cout << "请输入联系人的年龄：" << endl;
        cin >> age;
        abs->pArray[ret].age = age;
        string phone;
        cout << "请输入联系人的电话：" << endl;
        cin >> phone;
        abs->pArray[ret].phone = phone;
        string address;
        cout << "请输入联系人的住址：" << endl;
        cin >> address;
        abs->pArray[ret].address = address;
        cout << "修改成功！" << endl;
    }
};


void findPerson(struct AddressBook * abs){
    cout << "请输入要查找的联系人姓名：" << endl;
    string fName;
    cin >> fName;
    int ret = isExist(abs,fName);
    if(ret==-1){
        cout << "未找到该联系人！" << endl;
    }
    else{
        cout << "您要查找的联系人信息为：" << endl;
        cout << "姓名：" << abs->pArray[ret].name << "\t";
        cout << "性别：" << abs->pArray[ret].sex << "\t";
        cout << "电话：" << abs->pArray[ret].phone << "\t";
        cout << "住址：" <<abs->pArray[ret].address << endl;
    };
}

int main(){
    // 创建通讯录结构体比阿娘
    struct AddressBook aBook;
    aBook.size = 0; 
    int select = 0;
    while(true){
        //调用菜单
        showpage();
        cin >> select;
        switch (select)
        {
        case 1:
            addPerson(&aBook);     //利用地址传递，可以修饰实参
            break;
        case 2:
            showPerson(&aBook);
            break;
        case 3:
            deletePerson(&aBook);
            break;
        case 4:
            findPerson(&aBook);
            break;
        case 5:
            modifyPerson(&aBook);
            break;
        case 6:
            clearPerson(&aBook);
            break;
        default:

            break;
        }
    };
    pause();
    return 0;

}