using System;
using System.Collections.Generic;
using System.IO;

namespace Naveen
{
    public class FileManager
    {
        private readonly List<string> _files = new List<string>();

        public void AddFile(string path)
        {
            if (string.IsNullOrWhiteSpace(path))
            {
                throw new ArgumentException("File path cannot be null or empty.", nameof(path));
            }

            if (!File.Exists(path))
            {
                File.Create(path).Dispose();
            }

            _files.Add(path);
        }

        public IEnumerable<string> GetFiles()
        {
            return _files;
        }
    }
}
