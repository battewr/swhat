cmake_minimum_required(VERSION 3.16)
project(swhat VERSION 0.1.0 LANGUAGES NONE)

# Find required tools
find_program(UV_EXECUTABLE uv REQUIRED)
find_program(PYTHON_EXECUTABLE python3 python REQUIRED)

message(STATUS "UV executable: ${UV_EXECUTABLE}")
message(STATUS "Python executable: ${PYTHON_EXECUTABLE}")

# Build directory for artifacts
set(DIST_DIR "${CMAKE_SOURCE_DIR}/dist")

# Custom target: build - builds the Python package
add_custom_target(build
    COMMAND ${UV_EXECUTABLE} build
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Building swhat package..."
)

# Custom target: dev - installs package as a tool (globally available)
add_custom_target(dev
    COMMAND ${UV_EXECUTABLE} tool install --editable "${CMAKE_SOURCE_DIR}" --force
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Installing swhat in development mode..."
)

# Custom target: lint - runs the linter
add_custom_target(lint
    COMMAND ${UV_EXECUTABLE} tool run ruff check src/
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Running linter..."
)

# Custom target: format - formats code
add_custom_target(format
    COMMAND ${UV_EXECUTABLE} tool run ruff format src/
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Formatting code..."
)

# Install target - installs to system
install(CODE "
    execute_process(
        COMMAND ${UV_EXECUTABLE} pip install ${DIST_DIR}/swhat-${PROJECT_VERSION}-py3-none-any.whl --system
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        RESULT_VARIABLE result
    )
    if(NOT result EQUAL 0)
        message(FATAL_ERROR \"Failed to install swhat\")
    endif()
")

# Custom clean target for Python artifacts (named pyclean to avoid CMake reserved name)
# Note: __pycache__ cleanup is handled in platform-specific build scripts
add_custom_target(pyclean
    COMMAND ${CMAKE_COMMAND} -E rm -rf "${CMAKE_SOURCE_DIR}/dist"
    COMMAND ${CMAKE_COMMAND} -E rm -rf "${CMAKE_SOURCE_DIR}/src/swhat.egg-info"
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Cleaning Python artifacts..."
)

# Print usage info
message(STATUS "")
message(STATUS "swhat CMake build system")
message(STATUS "========================")
message(STATUS "")
message(STATUS "Usage:")
message(STATUS "  cmake -B build                    # Configure")
message(STATUS "  cmake --build build               # Build package")
message(STATUS "  cmake --build build --target dev  # Dev install")
message(STATUS "  cmake --build build --target lint # Run linter")
message(STATUS "  cmake --install build             # Install to system")
message(STATUS "  cmake --build build --target pyclean # Clean artifacts")
message(STATUS "")
