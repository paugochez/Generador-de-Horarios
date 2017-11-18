#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;


// Structure to define my subjects my name, credits and sign
struct subject {
  string sigla;
  string nombre;
  int creditos;
};

//Structure to define each available class
struct timeTable  {
  string day;
  string time;
  string classroom;
  subject eachClass;
};

//Function to generate Schedule
vector<timeTable> timeTableGenerator (vector<subject> classesLeft, int creditos, vector<timeTable> schedules )
{
  
}

// Function to trim .txt that contains subjects left
vector<subject*> trimFiles(string txtName){
  vector<subject*> subjectsLeft;
  string line;
  ifstream myfile (txtName);

  if (myfile.is_open())   //open and read file
    {
      while ( getline (myfile,line) )
	{
	  subject *newSubject = new subject;
	  string delimiter = "\t";
	  size_t pos = 0;
	  string token;
	  int count = 0;
	  
	  cout <<" Materia:" << endl;
	  
	  while ((pos = line.find(delimiter)) != string::npos) {  //Loop to trim .txt

	    
	    int limit = 3;  
	    token = line.substr(0, pos);
	    
	    if (count == 0){
	      newSubject->sigla = token;
	      cout << "\t Sigla:" << token << endl;
	    }
	    if (count == 1){
	      newSubject->nombre = token;
	      cout << "\t Nombre:" << token << endl;
	    }
	    if (count == 2){
	      cout << "\t error obteniendo creditos \n";
	    }
	      //newSubject->creditos = atoi(token);
	    line.erase(0, pos + delimiter.length());
	    count+=1;
	    
	    if (count == limit){
	      count = 0;
	      subjectsLeft.push_back(newSubject);
	      cout << "Size: "<< subjectsLeft.size();
	    }
	  }
	}
      myfile.close();
      
    }
  
  else cout << "Unable to open file";
  
  return subjectsLeft;
}


int main() {

  system("python3 ./bin/web_main.py b53375 @Manati666"); //bash call to run python underneath to obtain coursesLeft
  
  vector<subject*> subjectsLeft;

  subjectsLeft = trimFiles("cursos.txt");

  cout << "Size: "<< subjectsLeft.size();

  //cout << "La sigla del primer curso es" << subjectsLeft[0].sigla << endl ;
  return 0;
}




