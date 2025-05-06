using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Lex.Models;

public class Diary
{
    [Key]
    public int DiaryId { get; set; }
    
    public required string Content { get; set; } // JSON stored as string
    public required bool SentOver { get; set; }

    public int ClassToReference { get; set; }
    [ForeignKey("ClassToReference")]
    public required Class Class { get; set; }

    public DateTime DateOfReference { get; set; }
}