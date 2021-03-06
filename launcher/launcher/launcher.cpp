#include "stdafx.h"
#include <Windows.h>
#include <iostream>


int main()
{
   std::cout << "Launching" << std::endl;
   // additional information
   STARTUPINFO si;
   PROCESS_INFORMATION pi;

   // set the size of the structures
   ZeroMemory( &si, sizeof( si ) );
   si.cb = sizeof( si );
   ZeroMemory( &pi, sizeof( pi ) );

   // start the program up
   wchar_t b[] = L".\\venv\\Scripts\\python.exe .\\main.py";
   auto bSuccess = CreateProcess( L".\\venv\\Scripts\\python.exe",   // the path
      b,        // Command line
      NULL,           // Process handle not inheritable
      NULL,           // Thread handle not inheritable
      TRUE,          // Set handle inheritance to FALSE
      0,              // No creation flags
      NULL,           // Use parent's environment block
      NULL,           // Use parent's starting directory 
      &si,            // Pointer to STARTUPINFO structure
      &pi             // Pointer to PROCESS_INFORMATION structure (removed extra parentheses)
   );
   ShellExecute( 0, L"open", L"http://127.0.0.1:8080/index.html", 0, 0, SW_SHOW );
   if( !bSuccess )
   {
      std::cout << "Error spawning process";
   }
   else
   {
      // Close process and thread handles. 
      WaitForSingleObject( pi.hProcess, INFINITE );
      CloseHandle( pi.hProcess );
      CloseHandle( pi.hThread );
   }
   std::cin.get();
   return 0;
}

