#include<iostream>
using namespace std;
#include<unistd.h>

int main(){
    for(int i=1;i<10;i++)
    {
        for(int j=1;j<=i;j++)
        {
            cout << i << "*" << j << "=" << i*j << " ";
        }
        cout << endl;
    }
}