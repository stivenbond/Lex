using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Lex.Models;

public class Class
{
    [Key]
    public int ClassId { get; set; }

    public int Year { get; set; }
    public int Index { get; set; }
    [MaxLength(100)]
    public required string Subject { get; set; }

    public int CurrentLesson { get; set; }
    [ForeignKey("CurrentLesson")]
    public required Lesson Lesson { get; set; }

    public required ICollection<Diary> Diaries { get; set; }
}