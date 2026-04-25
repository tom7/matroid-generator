CXX := g++
CXXFLAGS := -O3 -march=native -funroll-loops -Wall -Wextra -Wpedantic -Wconversion
SHELL_CMD := bash
SRC_DIR := src
BUILD_DIR := build
TEST_DIR := tests
TARGET := $(BUILD_DIR)/IC
SZ := $(BUILD_DIR)/sz
MAKEPERM := $(BUILD_DIR)/makeperm

SRCS := $(filter-out $(SRC_DIR)/sz.cpp $(SRC_DIR)/makeperm.cpp, $(wildcard $(SRC_DIR)/*.cpp))
OBJS := $(patsubst $(SRC_DIR)/%.cpp,$(BUILD_DIR)/%.o,$(SRCS))
DEPS := $(OBJS:.o=.d) $(BUILD_DIR)/sz.d $(BUILD_DIR)/makeperm.d

all: $(TARGET) $(SZ) $(MAKEPERM)

$(TARGET): $(OBJS) | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -o $@ $^

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -MMD -MP -MF $(BUILD_DIR)/$*.d -c -o $@ $<

$(SZ): $(SRC_DIR)/sz.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -MMD -MP -MF $(BUILD_DIR)/sz.d -o $@ $<

$(MAKEPERM): $(SRC_DIR)/makeperm.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -MMD -MP -MF $(BUILD_DIR)/makeperm.d -o $@ $<

-include $(DEPS)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

test: all
	$(SHELL_CMD) $(TEST_DIR)/test.sh

format:
	clang-format -i $(SRCS) $(SRC_DIR)/sz.cpp $(wildcard $(SRC_DIR)/*.h)

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all test format clean
