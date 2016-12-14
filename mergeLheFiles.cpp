// modify outputfile in this code:
//  std::ofstream outFile("/afs/cern.ch/work/w/wshi/public/DisplacedMuonJetAnalysis_2016/CMSSW_8_0_20/src/DarkSUSY_mH_125_mN1_10_mGammaD_0p4_13TeV_cT_100_madgraph452_bridge224_events1500k.lhe", std::ios::out);
// g++ -Wall -o mergeLheFiles mergeLheFiles.cpp
// ls /eos/user/w/wshi/DarkSUSYMC_LHE_Moriond2017_Part2/DarkSUSY_mH_125_mN1_10_mGammaD_0p4_13TeV_cT_100_madgraph452_bridge224_events* > laMiaLista
// ./mergeLheFiles laMiaLista


#include <iostream>
#include <fstream>
#include <vector>
#include <string.h>
#include <stdio.h>

int main(int argc, char** argv)
{

  std::string line;
  std::string line2;
  /* if(argc < 3)
  {
    std::cout << ">>>splitLheFile.cpp::Usage:   " << argv[0] << "   initialFile.lhe   fileToAdd1.lhe   fileToAdd2.lhe ..." << std::endl;
    return -1;
    }*/
  
  char* fileListName = argv[1];
  std::ifstream fileList(fileListName, std::ios::in);
  int fileIt = 0;  

  char* initialFileName;
  std::vector<char*> fileToAddNames;

  while(!fileList.eof()) {
    getline(fileList, line);
    if( !fileList.good() ) break;

    char *cline = new char[line.length() + 1];
    strcpy(cline, line.c_str());
    if (fileIt==0) {
      initialFileName = cline;
      std::cout << "initialFileName = " << initialFileName << std::endl;
    } else {
      fileToAddNames.push_back( cline  );
      std::cout << "fileToAddName = " << fileToAddNames.at(fileIt-1) << std::endl;
    }
    fileIt++;
  }

  std::cout << "Merging " << fileIt << " LHE files" << std::endl;
  /* char* initialFileName = argv[1]; 
  std::cout << "initialFileName = " << initialFileName << std::endl;
  
  std::vector<char*> fileToAddNames;
  for(int fileIt = 0; fileIt < argc-2; ++fileIt)
  {
    fileToAddNames.push_back( argv[2+fileIt] );
    std::cout << "fileToAddName = " << fileToAddNames.at(fileIt) << std::endl;
    }  */
  
  
  // open lhe file
  std::ifstream initialFile(initialFileName, std::ios::in);
  std::ofstream outFile("/afs/cern.ch/work/w/wshi/public/DisplacedMuonJetAnalysis_2016/CMSSW_8_0_20/src/DarkSUSY_mH_125_mN1_10_mGammaD_0p4_13TeV_cT_100_madgraph452_bridge224_events1500k.lhe", std::ios::out);
  
 
  bool writeEvent = false;
  int eventIt = 0;
  
  while(!initialFile.eof())
  {
    getline(initialFile, line);
    if( !initialFile.good() ) break;
    
    if( line == "<LesHouchesEvents version=\"1.0\">" )
    {
      for(int fileIt2 = 0; fileIt2 < fileIt-1; ++fileIt2)
      {
        std::ifstream fileToAdd(fileToAddNames.at(fileIt2), std::ios::in);
        
        while(!fileToAdd.eof())
        {
          getline(fileToAdd, line2); 
          
          // decide whether to skip event or not 
          if( line2 == "<event>" )
          {
            ++eventIt;
            writeEvent = true;
          }
                
          
          // write line to outFile
          if(writeEvent == true)
            outFile << line2 << std::endl;
          
          
          // end of event
          if( line2 == "</event>" )
            writeEvent = false;
        }
      }
      break;
    }
    else outFile << line << std::endl;
    
  }
  outFile << "</LesHouchesEvents>" << std::endl;
  
  std::cout << "Added " << eventIt << " events from " << fileIt-1 << " files to file " << initialFileName << std::endl;
  return 0;
}
