export WORKING_DIRECTORY := $(CURDIR)
export INSTALL_PATH := ~/.config/systemd/user/embeddertg.service

install:
ifneq ("$(wildcard $(INSTALL_PATH))", "")
	@echo "Already installed"
	@echo "To uninstall: make uninstall"
else
	./scripts/mo embeddertg.service.mo > $(INSTALL_PATH)
	systemctl --user enable embeddertg
endif

uninstall:
ifneq ("$(wildcard $(INSTALL_PATH))", "")
	systemctl --user disable embeddertg
	rm $(INSTALL_PATH)
else
	@echo "Nothing to remove"
endif


