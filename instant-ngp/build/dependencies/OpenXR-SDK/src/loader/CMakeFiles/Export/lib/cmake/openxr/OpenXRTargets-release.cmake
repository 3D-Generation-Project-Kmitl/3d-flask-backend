#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "OpenXR::openxr_loader" for configuration "Release"
set_property(TARGET OpenXR::openxr_loader APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(OpenXR::openxr_loader PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libopenxr_loader.so.1.0.26"
  IMPORTED_SONAME_RELEASE "libopenxr_loader.so.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS OpenXR::openxr_loader )
list(APPEND _IMPORT_CHECK_FILES_FOR_OpenXR::openxr_loader "${_IMPORT_PREFIX}/lib/libopenxr_loader.so.1.0.26" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
