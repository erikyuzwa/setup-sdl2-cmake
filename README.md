# setup-sdl2-cmake
a bunch of CMake configuration files for handling SDL2

I'm (dumbly?) sometimes in a situation where I need to flip between SDL2 development
work on my Mac and PC. It's quite tricky setting up an environment that can handle
this "platform toggling" without headaches.

CMake provides an improvement - usually - to the process, allowing me to work
on the same codebase on PC / Mac.

## setting up

- Create a `CMake` compatible project in CLion or Visual Studio (on PC)
- Clone this repo so that the `cmake` folder is in your project's root folder (or download
this repository as a zip file)
- Update your local `CMakeLists.txt` with something close to what's here in the README

# sample CMakeLists.txt

```
cmake_minimum_required(VERSION 3.8)
project("helloworld")

set(CMAKE_CXX_STANDARD 11)

# use FindSDL2*.cmake scripts
set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_SOURCE_DIR}/bin")


if(WIN32)
  if(MSVC)
    # ensure we use minimal "windows.h" lib without the crazy min max macros
    SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /D \"WIN32_LEAN_AND_MEAN\"")
    SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /D \"NOMINMAX\"")
  endif(MSVC)
endif(WIN32)

# set SDL2 paths on windows
# TODO: THIS IS WHERE YOU DEFINE YOUR OWN SDL2 INSTALL
if(WIN32)
  set(SDL2_PATH "C:/SDL2-2.0.16")
  set(SDL2_TTF_PATH "c:/SDL2_ttf-2.0.15")
  set(SDL2_IMAGE_PATH "c:/SDL2_image-2.0.5")
  set(SDL2_MIXER_PATH "c:/SDL2_mixer-2.0.4")
endif(WIN32)

# Find SDL2, SDL2_image libraries
find_package(SDL2 REQUIRED)
find_package(SDL2_image REQUIRED)
find_package(SDL2_ttf REQUIRED)
find_package(SDL2_mixer REQUIRED)

include_directories(
    "src/"
    ${SDL2_INCLUDE_DIR}
    ${SDL2_TTF_INCLUDE_DIR}
    ${SDL2_IMAGE_INCLUDE_DIR}
    ${SDL2_MIXER_INCLUDE_DIR}
)

set(SOURCE_FILES
  "src/main.cpp"
)

# Add source to this project's executable.
if(WIN32)
  add_executable (${PROJECT_NAME} WIN32 ${SOURCE_FILES})
endif(WIN32)

if (APPLE)
  add_executable (${PROJECT_NAME} ${SOURCE_FILES})
endif(APPLE)

# Win32 needs to use SDL2_LIBRARIES to include SDL2main.lib
if(WIN32)
target_link_libraries(${PROJECT_NAME}
    ${SDL2_LIBRARIES}
    ${SDL2_TTF_LIBRARIES}
    ${SDL2_IMAGE_LIBRARIES}
    ${SDL2_MIXER_LIBRARIES}
)
endif(WIN32)

# Mac is fine with just SDL2_LIBRARY (using SDL2_LIBRARIES here complains about missing a
# Cocoa Framework lib)
if(APPLE)
  target_link_libraries(${PROJECT_NAME}
    ${SDL2_LIBRARY}
    ${SDL2_TTF_LIBRARIES}
    ${SDL2_IMAGE_LIBRARIES}
    ${SDL2_MIXER_LIBRARIES}
)
endif(APPLE)

# post build we need to copy the SDL DLL's from extern to our bin folder
if(WIN32)
  set( THIRD_PARTY_DLLS
    ${SDL2_PATH}/${VC_LIB_PATH_SUFFIX}/SDL2.dll
    ${SDL2_IMAGE_PATH}/${VC_LIB_PATH_SUFFIX}/SDL2_image.dll
    ${SDL2_IMAGE_PATH}/${VC_LIB_PATH_SUFFIX}/libjpeg-9.dll
    ${SDL2_IMAGE_PATH}/${VC_LIB_PATH_SUFFIX}/libpng16-16.dll
    ${SDL2_TTF_PATH}/${VC_LIB_PATH_SUFFIX}/SDL2_ttf.dll
    ${SDL2_TTF_PATH}/${VC_LIB_PATH_SUFFIX}/libfreetype-6.dll
    ${SDL2_TTF_PATH}/${VC_LIB_PATH_SUFFIX}/zlib1.dll
    ${SDL2_MIXER_PATH}/${VC_LIB_PATH_SUFFIX}/SDL2_mixer.dll
    ${SDL2_MIXER_PATH}/${VC_LIB_PATH_SUFFIX}/libogg-0.dll
  )

  # copy the DLLs
  foreach( file_i ${THIRD_PARTY_DLLS})
    add_custom_command(
            TARGET ${PROJECT_NAME} POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy ${file_i} "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}"
    )
  endforeach( file_i )

endif(WIN32)

# Scan through assets folder for updated files and copy if none existing or changed
file (GLOB_RECURSE assets "assets/*.*")
foreach(asset ${assets})
 get_filename_component(filename ${asset} NAME)
 get_filename_component(dir ${asset} DIRECTORY)
 get_filename_component(dirname ${dir} NAME)
 
 set (output "")
 
 while(NOT ${dirname} STREQUAL assets)
  get_filename_component(path_component ${dir} NAME)
  set (output "${path_component}/${output}")
  get_filename_component(dir ${dir} DIRECTORY)
  get_filename_component(dirname ${dir} NAME)
 endwhile()
 
 set(output "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/assets/${output}/${filename}")
 
 add_custom_command(
  COMMENT "Moving updated resource-file '${filename}'"
  OUTPUT ${output}
  DEPENDS ${asset}
  COMMAND ${CMAKE_COMMAND} -E copy_if_different
  ${asset}
  ${output}
 )
 add_custom_target(${filename} ALL DEPENDS ${asset} ${output})
 
endforeach()

```

# REFERENCES

Many CMake SDL2 tutorials were scoured to consolidate this info, definitely
couldn't have done it without them:

- https://gitlab.com/aminosbh/sdl2-cmake-modules
- https://trenki2.github.io/blog/2017/06/02/using-sdl2-with-cmake/
- https://shot511.github.io/2018-05-29-how-to-setup-opengl-project-with-cmake/
- https://stackoverflow.com/questions/14368919/cmake-custom-command-copy-multiple-files

# LICENSE

MIT License

Copyright (c) 2020 Erik Yuzwa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.