using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Lex.Models;

public class File
{
    [Key]
    public int FileId { get; set; }

    public int LessonId { get; set; }
    [ForeignKey("LessonId")]
    public required Lesson Lesson { get; set; }

    public required byte[] Content { get; set; }

    public required string Type { get; set; }
}
