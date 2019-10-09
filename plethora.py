#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.app import App

if __name__ == '__main__':
    import os
    print(os.getcwd())
    app = App()
    app.run()
