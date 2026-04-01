import re

with open("C:/Users/Admin0x/AppData/Local/Temp/hadris-fat/crates/hadris-fat/src/exfat/fs.rs", "r") as f:
    content = f.read()

# Add create_file_with_timestamps after create_file
insert_after = """        })
    }

    /// Create a new directory.
    ///
    /// Note: Unlike FAT, exFAT directories don't have . and .. entries."""

new_methods = """        })
    }

    /// Create a new file with custom timestamps.
    pub fn create_file_with_timestamps(
        &self,
        parent: &ExFatDir<'_, DATA>,
        name: &str,
        created: super::time::ExFatTimestamp,
        modified: super::time::ExFatTimestamp,
        accessed: super::time::ExFatTimestamp,
    ) -> Result<ExFatFileEntry> {
        if parent.find(name)?.is_some() {
            return Err(FatError::AlreadyExists);
        }

        let builder = EntrySetBuilder::file(name)?
            .with_timestamps(created.clone(), modified.clone(), accessed.clone());
        let entries = builder.build(&self.upcase);
        let entry_count = entries.len();

        let (slot_cluster, slot_offset) = self.find_free_entry_slots(parent, entry_count)?;
        self.write_entry_set(slot_cluster, slot_offset, &entries)?;

        Ok(ExFatFileEntry {
            name: name.to_string(),
            attributes: FileAttributes::ARCHIVE,
            first_cluster: 0,
            data_length: 0,
            valid_data_length: 0,
            no_fat_chain: true,
            name_hash: self.upcase.name_hash(name),
            created,
            modified,
            accessed,
            parent_cluster: slot_cluster,
            entry_offset: self.info.cluster_to_offset(slot_cluster) + slot_offset,
        })
    }

    /// Create a new directory with custom timestamps.
    pub fn create_dir_with_timestamps(
        &self,
        parent: &ExFatDir<'_, DATA>,
        name: &str,
        created: super::time::ExFatTimestamp,
        modified: super::time::ExFatTimestamp,
        accessed: super::time::ExFatTimestamp,
    ) -> Result<ExFatDir<'_, DATA>> {
        if parent.find(name)?.is_some() {
            return Err(FatError::AlreadyExists);
        }

        let dir_cluster = self.allocate_cluster(2)?;
        let cluster_offset = self.info.cluster_to_offset(dir_cluster);
        let zeros = alloc::vec![0u8; self.info.bytes_per_cluster];
        self.write_at(cluster_offset, &zeros)?;

        let builder = EntrySetBuilder::directory(name)?
            .with_cluster(dir_cluster)
            .with_size(0, self.info.bytes_per_cluster as u64)
            .with_contiguous(true)
            .with_timestamps(created, modified, accessed);
        let entries = builder.build(&self.upcase);
        let entry_count = entries.len();

        let (slot_cluster, slot_offset) = self.find_free_entry_slots(parent, entry_count)?;
        self.write_entry_set(slot_cluster, slot_offset, &entries)?;

        self.sync_bitmap()?;
        let _ = self.flush();

        Ok(ExFatDir::new(self, dir_cluster))
    }

    /// Create a new directory.
    ///
    /// Note: Unlike FAT, exFAT directories don't have . and .. entries."""

content = content.replace(insert_after, new_methods, 1)

with open("C:/Users/Admin0x/AppData/Local/Temp/hadris-fat/crates/hadris-fat/src/exfat/fs.rs", "w") as f:
    f.write(content)

print("Patched successfully")
