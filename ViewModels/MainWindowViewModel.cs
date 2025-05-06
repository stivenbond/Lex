using ReactiveUI;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Reactive;
using System.Reactive.Linq;

namespace Lex.ViewModels
{
    public class MainWindowViewModel : ViewModelBase
    {
        // Properties for main layout state
        public required bool _isSplitView;
        public bool IsSplitView
        {
            get => _isSplitView;
            set => this.RaiseAndSetIfChanged(ref _isSplitView, value);
        }

        public required bool _isLeftSidebarVisible;
        public bool IsLeftSidebarVisible
        {
            get => _isLeftSidebarVisible;
            set => this.RaiseAndSetIfChanged(ref _isLeftSidebarVisible, value);
        }

        public required bool _isRightSidebarVisible;
        public bool IsRightSidebarVisible
        {
            get => _isRightSidebarVisible;
            set => this.RaiseAndSetIfChanged(ref _isRightSidebarVisible, value);
        }

        // View models for different content types
        public required ViewModelBase _leftContentViewModel;
        public ViewModelBase LeftContentViewModel
        {
            get => _leftContentViewModel;
            set => this.RaiseAndSetIfChanged(ref _leftContentViewModel, value);
        }

        public required ViewModelBase _rightContentViewModel;
        public ViewModelBase RightContentViewModel
        {
            get => _rightContentViewModel;
            set => this.RaiseAndSetIfChanged(ref _rightContentViewModel, value);
        }

        // Commands for menu actions
        public ReactiveCommand<Unit, bool> ToggleLeftSidebarCommand { get; }
        public ReactiveCommand<Unit, bool> ToggleRightSidebarCommand { get; }
        public ReactiveCommand<Unit, bool> ToggleSplitViewCommand { get; }
        
        // Commands for content type switching
        public ReactiveCommand<Unit, ViewModelBase> ShowTextDocumentCommand { get; }
        public ReactiveCommand<Unit, ViewModelBase> ShowSlideshowCommand { get; }
        public ReactiveCommand<Unit, ViewModelBase> ShowWebReferenceCommand { get; }
        public ReactiveCommand<Unit, ViewModelBase> ShowTestViewCommand { get; }

        public MainWindowViewModel()
        {
            // Initialize sidebar visibility
            IsLeftSidebarVisible = true;
            IsRightSidebarVisible = false;
            IsSplitView = false;

            // Set default content
            LeftContentViewModel = new TextDocumentViewModel
            {
                _documentText = null
            };

            // Initialize commands
            ToggleLeftSidebarCommand = ReactiveCommand.Create(() => 
                IsLeftSidebarVisible = !IsLeftSidebarVisible);
            
            ToggleRightSidebarCommand = ReactiveCommand.Create(() => 
                IsRightSidebarVisible = !IsRightSidebarVisible);
            
            ToggleSplitViewCommand = ReactiveCommand.Create(() => 
                IsSplitView = !IsSplitView);
            
            ShowTextDocumentCommand = ReactiveCommand.Create(() => 
                LeftContentViewModel = new TextDocumentViewModel
                {
                    _documentText = null
                });
            
            ShowSlideshowCommand = ReactiveCommand.Create(() => 
                LeftContentViewModel = new SlideshowViewModel
                {
                    _slides = null
                });
            
            ShowWebReferenceCommand = ReactiveCommand.Create(() => 
                LeftContentViewModel = new WebReferenceViewModel
                {
                    _url = null
                });
            
            ShowTestViewCommand = ReactiveCommand.Create(() => 
                LeftContentViewModel = new TestViewModel
                {
                    _questions = null
                });
        }
    }
}
