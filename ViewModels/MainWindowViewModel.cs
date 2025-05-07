using Lex.Data;
using Lex.Data.Repositories;
using SQLitePCL;

namespace Lex.ViewModels;

public class MainWindowViewModel()
{
    public required LeftSidebarViewModel LeftSidebarViewModel { get; set; }

    public MainWindowViewModel(LeftSidebarViewModel leftSidebarViewModel) : this()
    {
        LeftSidebarViewModel = leftSidebarViewModel;
    }


}